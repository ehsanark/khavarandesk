#!/usr/bin/env bash
set -euo pipefail

PREFIX="/opt/khavarandesk-server"
STATE_DIR="/var/lib/khavarandesk-server"
CONF_DIR="/etc/khavarandesk-server"
SERVICE_USER="khavarandesk"
SERVICE_GROUP="khavarandesk"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run this installer as root: sudo ./install.sh" >&2
  exit 1
fi

for bin in hbbs hbbr; do
  if [[ ! -f "${SCRIPT_DIR}/bin/${bin}" ]]; then
    echo "Missing ${SCRIPT_DIR}/bin/${bin}. Use an official Khavaran Desk Server release bundle." >&2
    exit 1
  fi
done

if ! getent group "${SERVICE_GROUP}" >/dev/null; then
  groupadd --system "${SERVICE_GROUP}"
fi
if ! id -u "${SERVICE_USER}" >/dev/null 2>&1; then
  useradd --system --gid "${SERVICE_GROUP}" --home-dir "${STATE_DIR}" --shell /usr/sbin/nologin "${SERVICE_USER}"
fi

install -d -m 0755 "${PREFIX}/bin"
install -d -o "${SERVICE_USER}" -g "${SERVICE_GROUP}" -m 0750 "${STATE_DIR}"
install -d -m 0755 "${CONF_DIR}"

install -m 0755 "${SCRIPT_DIR}/bin/hbbs" "${PREFIX}/bin/hbbs"
install -m 0755 "${SCRIPT_DIR}/bin/hbbr" "${PREFIX}/bin/hbbr"
install -m 0644 "${SCRIPT_DIR}/VERSION" "${PREFIX}/VERSION"
install -m 0644 "${SCRIPT_DIR}/UPSTREAM_VERSION" "${PREFIX}/UPSTREAM_VERSION"
install -m 0644 "${SCRIPT_DIR}/LICENSE" "${PREFIX}/LICENSE"
install -m 0755 "${SCRIPT_DIR}/khavaran-server" "/usr/local/bin/khavaran-server"

install -m 0644 "${SCRIPT_DIR}/systemd/khavaran-hbbs.service" "/etc/systemd/system/khavaran-hbbs.service"
install -m 0644 "${SCRIPT_DIR}/systemd/khavaran-hbbr.service" "/etc/systemd/system/khavaran-hbbr.service"

if [[ ! -f "${CONF_DIR}/server.env" ]]; then
  cat > "${CONF_DIR}/server.env" <<'EOF'
# Optional command-line arguments.
# Example when your relay is relay.example.com:
# HBBS_ARGS=-r relay.example.com:21117
HBBS_ARGS=
HBBR_ARGS=
RUST_LOG=info
EOF
  chmod 0600 "${CONF_DIR}/server.env"
fi

chown -R "${SERVICE_USER}:${SERVICE_GROUP}" "${STATE_DIR}"

systemctl daemon-reload
systemctl enable --now khavaran-hbbr.service
systemctl enable --now khavaran-hbbs.service

sleep 2
failed=0
for unit in khavaran-hbbr.service khavaran-hbbs.service; do
  if ! systemctl is-active --quiet "${unit}"; then
    echo "${unit} failed to start." >&2
    systemctl --no-pager --full status "${unit}" || true
    failed=1
  fi
done
if [[ ${failed} -ne 0 ]]; then
  exit 1
fi

for _ in {1..10}; do
  [[ -s "${STATE_DIR}/id_ed25519.pub" ]] && break
  sleep 1
done

echo
echo "Khavaran Desk Server installed successfully."
echo "Services: khavaran-hbbs, khavaran-hbbr"
echo "State:    ${STATE_DIR}"
echo "Config:   ${CONF_DIR}/server.env"
echo
echo "Required firewall ports:"
echo "  TCP 21115-21119"
echo "  UDP 21116"
echo
echo "Client configuration:"
echo "  ID Server:    <this server public IP or hostname>"
echo "  Relay Server: <this server public IP or hostname>"
echo "  API Server:   leave blank for OSS server"
if [[ -s "${STATE_DIR}/id_ed25519.pub" ]]; then
  echo -n "  Key:          "
  cat "${STATE_DIR}/id_ed25519.pub"
else
  echo "  Key:          run: sudo khavaran-server key"
fi
echo
echo "Use 'sudo khavaran-server info' for a summary."
