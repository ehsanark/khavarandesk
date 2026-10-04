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

Then configure the client:

- ID Server: public hostname or IP of your server
- Relay Server: public hostname or IP of your server
- API Server: leave blank for the OSS server
- Key: output of `sudo khavaran-server key`

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
