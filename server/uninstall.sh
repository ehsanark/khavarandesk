#!/usr/bin/env bash
set -euo pipefail

PREFIX="/opt/khavarandesk-server"
STATE_DIR="/var/lib/khavarandesk-server"
CONF_DIR="/etc/khavarandesk-server"

if [[ ${EUID} -ne 0 ]]; then
  echo "Please run as root: sudo ./uninstall.sh [--purge]" >&2
  exit 1
fi

systemctl disable --now khavaran-hbbs.service khavaran-hbbr.service 2>/dev/null || true
rm -f /etc/systemd/system/khavaran-hbbs.service
rm -f /etc/systemd/system/khavaran-hbbr.service
systemctl daemon-reload
systemctl reset-failed 2>/dev/null || true

rm -rf "${PREFIX}"
rm -f /usr/local/bin/khavaran-server

if [[ "${1:-}" == "--purge" ]]; then
  rm -rf "${STATE_DIR}" "${CONF_DIR}"
  userdel khavarandesk 2>/dev/null || true
  groupdel khavarandesk 2>/dev/null || true
  echo "Khavaran Desk Server removed, including keys and database."
else
  echo "Khavaran Desk Server removed. Data and keys were preserved in ${STATE_DIR}."
  echo "Run './uninstall.sh --purge' if you also want to remove persistent data."
fi
