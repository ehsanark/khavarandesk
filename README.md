# Khavaran Desk

Khavaran Desk is a self-hosted remote desktop package built around RustDesk OSS, with a branded desktop client and deployable server bundles.

## Downloads

### Windows client

Current published Windows client:

- [KhavaranDesk-Setup-x64.exe](https://github.com/ehsanark/khavarandesk/releases/download/windows-build-4/KhavaranDesk-Setup-x64.exe)
- [Windows build 4 release](https://github.com/ehsanark/khavarandesk/releases/tag/windows-build-4)

The Persian/RTL client redesign is being validated separately before replacing the published Windows build.

### Khavaran Desk Server 1.0.0

Based on verified RustDesk Server OSS 1.1.16 binaries.

- [Linux x64 / amd64](https://github.com/ehsanark/khavarandesk/releases/download/server-v1.0.0-rd1.1.16/KhavaranDesk-Server-Linux-x64.tar.gz)
- [Linux ARM64 / Jetson](https://github.com/ehsanark/khavarandesk/releases/download/server-v1.0.0-rd1.1.16/KhavaranDesk-Server-Linux-ARM64.tar.gz)
- [SHA256SUMS](https://github.com/ehsanark/khavarandesk/releases/download/server-v1.0.0-rd1.1.16/SHA256SUMS)
- [Server release page](https://github.com/ehsanark/khavarandesk/releases/tag/server-v1.0.0-rd1.1.16)

Server packaging documentation is in [server/README.md](server/README.md).

## Quick server install

Example for Linux x64:

```bash
tar -xzf KhavaranDesk-Server-Linux-x64.tar.gz
cd KhavaranDesk-Server-Linux-x64
sudo ./install.sh
sudo khavaran-server info
```

For ARM64 or Jetson, use the ARM64 bundle instead.

Open these firewall ports:

- TCP 21115-21119
- UDP 21116

Windows and Jetson clients use a compiled, managed connection policy:

| Setting | Fixed value |
| --- | --- |
| ID server | `it-desk.khavaranai.ir` (port 21116) |
| Relay server | `it-desk.khavaranai.ir:21117` |
| API server | `https://it-desk.khavaranai.ir:8443` |
| Public key | `SNngVLEdOKKSsMzQuqQwT1EFjftRAVxfHBQSyOss1Zg=` |

The native core enforces these values over saved settings, configuration imports,
custom-client settings and Windows executable-name overrides. The desktop home
screen no longer displays the server address or a network setup shortcut. The
ID/Relay dialog is hidden and its entry points are guarded. Other settings,
including security and proxy settings, remain available.

`build/network.patch` applies after the pinned upstream and UI patches in every
client build. Native regression tests are in the patched `hbb_common` module:
`cargo test -p hbb_common khavaran_network_tests -- --test-threads=1`.

The API URL requires an actual RustDesk-compatible API service on port 8443;
a working HTTPS site alone is not sufficient. ID/relay connections still use
their native protocol and ports. TLS validation is not disabled. Install the
server certificate and private key only on the HTTPS server, never in the client.
The supplied public key is the hbbs public key, not a TLS certificate.

Hiding settings is a product policy, not secrecy: a server address and public key
can be recovered from a binary, source or network traffic. DNS must resolve the
hostname to the intended server, and hbbs must advertise a reachable relay.
Existing published installers are unchanged until new builds are produced.

## Server layout

The installer creates:

- `khavaran-hbbs.service` — ID/Rendezvous server
- `khavaran-hbbr.service` — relay server
- `/opt/khavarandesk-server` — binaries and package metadata
- `/var/lib/khavarandesk-server` — database and cryptographic keys
- `/etc/khavarandesk-server/server.env` — optional server arguments
- `/usr/local/bin/khavaran-server` — status/key/log/restart helper

Server state and keys are preserved during a normal uninstall.

## Client source

The desktop client is built from pinned RustDesk source with Khavaran Desk changes applied by the repository build pipeline.

Pinned client upstream commit:

```
a7f2260203befb7e9c70b585219f0f0b5ca57703
```

Windows installers are currently unsigned.

## License and upstream attribution

License: AGPL-3.0.

Khavaran Desk retains the relevant RustDesk / Purslane copyright and license notices. The server release bundles use unmodified official RustDesk Server OSS hbbs/hbbr binaries; Khavaran Desk adds packaging, installation scripts, systemd services, verification, and documentation.
