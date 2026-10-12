# Khavaran Desk Server

بسته سرور خاوران دسک بر پایه RustDesk Server OSS ساخته می‌شود. باینری‌های `hbbs` و `hbbr` از Release رسمی RustDesk Server دریافت و SHA256 آن‌ها در GitHub Actions بررسی می‌شود؛ بسته خاوران نصب، سرویس‌های systemd و ابزار مدیریت را اضافه می‌کند.

## خروجی‌ها

- `KhavaranDesk-Server-Linux-x64.tar.gz` برای Linux x86_64 / amd64
- `KhavaranDesk-Server-Linux-ARM64.tar.gz` برای Linux ARM64 و Jetson Orin

نسخه بسته در `VERSION` و نسخه بالادستی RustDesk Server در `UPSTREAM_VERSION` پین شده است.

## نصب

```bash
tar -xzf KhavaranDesk-Server-Linux-x64.tar.gz
cd KhavaranDesk-Server-Linux-x64
sudo ./install.sh
```

روی Jetson/ARM64 نام فایل ARM64 را جایگزین کنید.

بعد از نصب:

```bash
sudo khavaran-server info
sudo khavaran-server status
sudo khavaran-server key
```

## تنظیم کلاینت خاوران

در بخش «تعریف و معرفی سرور» کلاینت:

- **ID Server:** دامنه یا IP عمومی همین سرور
- **Relay Server:** دامنه یا IP عمومی همین سرور
- **API Server:** در نسخه OSS خالی بماند
- **Key:** خروجی `sudo khavaran-server key`

## پورت‌های فایروال

برای استقرار معمولی RustDesk Server OSS این پورت‌ها باید از اینترنت به سرور قابل دسترس باشند:

- TCP: `21115-21119`
- UDP: `21116`

مثال UFW:

```bash
sudo ufw allow 21115:21119/tcp
sudo ufw allow 21116/udp
```

نصب‌کننده عمداً فایروال سیستم را خودکار تغییر نمی‌دهد.

## تنظیمات پیشرفته

فایل زیر بعد از نصب ایجاد می‌شود:

```
/etc/khavarandesk-server/server.env
```

برای نمونه، اگر Relay روی یک نام دامنه مشخص قرار دارد:

```bash
HBBS_ARGS=-r relay.example.com:21117
HBBR_ARGS=
RUST_LOG=info
```

سپس:

```bash
sudo khavaran-server restart
```

## داده‌ها و کلیدها

پایگاه داده و کلیدهای سرور در مسیر زیر نگهداری می‌شوند:

```
/var/lib/khavarandesk-server
```

در حذف عادی این پوشه پاک نمی‌شود تا IDها و کلیدها از بین نروند. برای حذف کامل:

```bash
sudo ./uninstall.sh --purge
```

## منبع و مجوز

Khavaran Desk Server از RustDesk Server OSS استفاده می‌کند و مجوز AGPL-3.0 و اعلان‌های کپی‌رایت بالادستی حفظ می‌شوند.


## مهاجرت از RustDesk Server موجود

برای حفظ کلید تنظیم‌شده در کلاینت‌ها، سرور باید کلید خصوصی متناظر را داشته باشد. از روی کلید عمومی نمی‌توان آن را ساخت. نصب تازه کلید جدید ایجاد می‌کند؛ در صورت تفاوت، نصب‌کننده هشدار می‌دهد و باید کلید واقعی سرور در تنظیمات کلاینت ثبت شود یا هویت قبلی منتقل شود.

برای مسیرهای غیر استاندارد (مثلاً volume کانتینر)، ابتدا سرویس/کانتینر قدیمی را در زمان مناسب متوقف کنید و سپس اجرا کنید:

```bash
sudo ./install.sh /absolute/path/to/existing/server/data
```

هر دو فایل کلید باید موجود باشند. هویت موجود خاوران بازنویسی نمی‌شود. پایگاه داده با SQLite backup و حفظ داده‌های WAL کپی می‌شود. برای مهاجرت پایگاه داده `python3` لازم است. نصب مجدد سرویس‌های خاوران را برای بارگذاری باینری جدید راه‌اندازی مجدد می‌کند.

آدرس اعلام‌شده Relay در نصب جدید `2.181.250.249:21117` است؛ روی VPS با آدرس متفاوت، مقدار `HBBS_ARGS` را تغییر دهید.

اگر روی VPS از قبل RustDesk Server OSS در مسیر استاندارد `/var/lib/rustdesk-server` نصب باشد، نصب‌کننده Khavaran Desk Server در صورتی که هنوز هویت جدیدی ساخته نشده باشد، این موارد را به‌صورت کپی حفظ می‌کند:

- `id_ed25519`
- `id_ed25519.pub`
- `db_v2.sqlite3` در صورت وجود

به این ترتیب Public Key قبلی سرور حفظ می‌شود و کلاینت‌هایی که با همان Key ساخته شده‌اند همچنان به همان سرور متصل می‌شوند. کلید خصوصی هرگز داخل ریپو یا کلاینت قرار نمی‌گیرد.
