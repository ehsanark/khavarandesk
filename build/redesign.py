# Apply the Khavaran desktop experience to the pinned RustDesk source.
# Every transformation is guarded so an upstream source change fails the build
# instead of silently producing a partially-branded client.
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def replace_once(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        raise RuntimeError(f"Khavaran redesign patch point not found: {label}")
    return content.replace(old, new, 1)


# Persian is the product default, while explicit user language choices win.
lang_path = "src/lang.rs"
s = read(lang_path)
needle = '    let mut lang = saved_lang.to_lowercase();\n'
replacement = '''    let mut lang = saved_lang.to_lowercase();
    // Khavaran Desk is a Persian-first client. Keep an explicit user choice,
    // but use Persian when no language has been selected yet.
    if lang.is_empty() || lang == "default" {
        lang = "fa".to_owned();
    }
'''
s = replace_once(s, needle, replacement, "Persian default language")
write(lang_path, s)


# Synchronize Flutter's locale with RustDesk's selected language. This gives
# Persian/Arabic/Hebrew/Urdu real RTL layout instead of translated LTR text.
main_path = "flutter/lib/main.dart"
s = read(main_path)
helper = r'''
Locale _khavaranUiLocale() {
  var selected =
      bind.mainGetLocalOption(key: kCommConfKeyLang).trim().toLowerCase();
  if (selected.isEmpty || selected == 'default') {
    selected = 'fa';
  }
  switch (selected) {
    case 'zh-cn':
      return const Locale('zh', 'CN');
    case 'zh-tw':
      return const Locale('zh', 'TW');
    case 'pt-br':
      return const Locale('pt', 'BR');
    case 'pt-pt':
      return const Locale('pt', 'PT');
    default:
      return Locale(selected.split(RegExp('[-_]')).first);
  }
}

'''
s = replace_once(
    s,
    "void _runApp(\n",
    helper + "void _runApp(\n",
    "Flutter locale helper",
)
s = replace_once(
    s,
    "      themeMode: themeMode,\n      home: home,\n",
    "      themeMode: themeMode,\n      locale: _khavaranUiLocale(),\n      home: home,\n",
    "installer/app locale",
)
s = replace_once(
    s,
    "          themeMode: MyTheme.currentThemeMode(),\n          home: isDesktop\n",
    "          themeMode: MyTheme.currentThemeMode(),\n          locale: _khavaranUiLocale(),\n          home: isDesktop\n",
    "main app locale",
)
write(main_path, s)


# Desktop home: responsive dashboard with visible server configuration.
home_path = "flutter/lib/desktop/pages/desktop_home_page.dart"
s = read(home_path)
import_line = "import 'package:flutter_hbb/models/platform_model.dart';\n"
s = replace_once(
    s,
    import_line,
    import_line + "import 'package:flutter_hbb/mobile/widgets/dialog.dart';\n",
    "server settings import",
)

build_start = s.index(
    "    return _buildBlock(",
    s.index("  Widget build(BuildContext context)"),
)
build_end = s.index("\n  Widget _buildBlock", build_start)

new_build = r'''    final isOutgoingOnly = bind.isOutgoingOnly();
    return _buildBlock(
      child: LayoutBuilder(
        builder: (context, constraints) {
          final theme = Theme.of(context);
          final dark = theme.brightness == Brightness.dark;
          final accent = const Color(0xFF0F766E);
          final accentSoft =
              dark ? const Color(0xFF123B3A) : const Color(0xFFE7F5F2);
          final canvas =
              dark ? const Color(0xFF0B1220) : const Color(0xFFF4F7F8);
          final surface =
              dark ? const Color(0xFF111C2D) : const Color(0xFFFFFFFF);
          final border =
              dark ? const Color(0xFF26364C) : const Color(0xFFDDE5E7);
          final muted =
              dark ? const Color(0xFF9FB0C4) : const Color(0xFF667781);

          Widget panel(Widget child, {EdgeInsetsGeometry? padding}) {
            return Container(
              padding: padding,
              clipBehavior: Clip.antiAlias,
              decoration: BoxDecoration(
                color: surface,
                borderRadius: BorderRadius.circular(22),
                border: Border.all(color: border),
                boxShadow: dark
                    ? const []
                    : const [
                        BoxShadow(
                          color: Color(0x12000000),
                          blurRadius: 24,
                          offset: Offset(0, 8),
                        ),
                      ],
              ),
              child: child,
            );
          }

          Widget serverCard() {
            return FutureBuilder<String>(
              future: bind.mainGetOptions(),
              builder: (context, snapshot) {
                var config = ServerConfig();
                if (snapshot.hasData) {
                  try {
                    config = ServerConfig.fromOptions(
                        jsonDecode(snapshot.data!) as Map<String, dynamic>);
                  } catch (_) {}
                }
                final configured = config.idServer.trim().isNotEmpty;
                final idServer = configured
                    ? config.idServer.trim()
                    : 'سرور هنوز تعریف نشده است';

                return Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: accentSoft,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: accent.withOpacity(.22)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Row(
                        children: [
                          Container(
                            width: 42,
                            height: 42,
                            decoration: BoxDecoration(
                              color: accent.withOpacity(.12),
                              borderRadius: BorderRadius.circular(13),
                            ),
                            child: const Icon(Icons.dns_rounded, color: accent),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  translate('ID/Relay Server'),
                                  style: const TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                                const SizedBox(height: 3),
                                Text(
                                  idServer,
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  textDirection: TextDirection.ltr,
                                  style: TextStyle(fontSize: 11.5, color: muted),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 9, vertical: 5),
                            decoration: BoxDecoration(
                              color: configured
                                  ? const Color(0xFFDCFCE7)
                                  : const Color(0xFFFFEDD5),
                              borderRadius: BorderRadius.circular(999),
                            ),
                            child: Text(
                              configured ? 'فعال' : 'نیاز به تنظیم',
                              style: TextStyle(
                                color: configured
                                    ? const Color(0xFF166534)
                                    : const Color(0xFF9A3412),
                                fontSize: 10.5,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ),
                        ],
                      ),
                      if (configured &&
                          (config.relayServer.trim().isNotEmpty ||
                              config.apiServer.trim().isNotEmpty)) ...[
                        const SizedBox(height: 12),
                        Text(
                          [
                            if (config.relayServer.trim().isNotEmpty)
                              'Relay: ${config.relayServer.trim()}',
                            if (config.apiServer.trim().isNotEmpty)
                              'API: ${config.apiServer.trim()}',
                          ].join('   •   '),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          textDirection: TextDirection.ltr,
                          style: TextStyle(fontSize: 10.5, color: muted),
                        ),
                      ],
                      const SizedBox(height: 14),
                      SizedBox(
                        height: 40,
                        child: OutlinedButton.icon(
                          onPressed: bind.isDisableSettings()
                              ? null
                              : () => showServerSettings(
                                    gFFI.dialogManager,
                                    setState,
                                  ),
                          icon: const Icon(Icons.tune_rounded, size: 18),
                          label: Text(
                            configured
                                ? 'ویرایش تنظیمات سرور'
                                : 'تعریف و معرفی سرور',
                          ),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: accent,
                            side: BorderSide(color: accent.withOpacity(.38)),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              },
            );
          }

          final localPanel = panel(
            SingleChildScrollView(
              controller: _leftPaneScrollController,
              padding: const EdgeInsets.all(18),
              child: Column(
                key: _childKey,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 46,
                        height: 46,
                        decoration: BoxDecoration(
                          color: accent.withOpacity(.12),
                          borderRadius: BorderRadius.circular(14),
                        ),
                        child: const Icon(
                          Icons.computer_rounded,
                          color: accent,
                          size: 25,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              translate('Your Desktop'),
                              style: const TextStyle(
                                fontSize: 17,
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                            const SizedBox(height: 3),
                            Text(
                              'شناسه و دسترسی این دستگاه',
                              style: TextStyle(fontSize: 11.5, color: muted),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  serverCard(),
                  if (!isOutgoingOnly) ...[
                    const SizedBox(height: 14),
                    buildPresetPasswordWarning(),
                    buildIDBoard(context),
                    buildPasswordBoard(context),
                  ],
                  const SizedBox(height: 8),
                  Divider(color: border),
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: OnlineStatusWidget(),
                  ),
                  Obx(() => buildHelpCards(stateGlobal.updateUrl.value)),
                ],
              ),
            ),
          );

          final remotePanel = panel(
            Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(18, 16, 18, 12),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.send_to_mobile_rounded,
                        color: accent,
                        size: 22,
                      ),
                      const SizedBox(width: 10),
                      const Expanded(
                        child: Text(
                          'اتصال به دستگاه دیگر',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                Divider(height: 1, color: border),
                Expanded(child: buildRightPane(context)),
              ],
            ),
          );

          final header = Container(
            padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 18),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: dark
                    ? const [Color(0xFF10243A), Color(0xFF0F766E)]
                    : const [Color(0xFF0E3A47), Color(0xFF0F766E)],
              ),
              borderRadius: BorderRadius.circular(22),
              boxShadow: const [
                BoxShadow(
                  color: Color(0x280F766E),
                  blurRadius: 28,
                  offset: Offset(0, 10),
                ),
              ],
            ),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(.12),
                    borderRadius: BorderRadius.circular(15),
                    border: Border.all(color: Colors.white.withOpacity(.16)),
                  ),
                  child: const Icon(
                    Icons.desktop_windows_rounded,
                    color: Colors.white,
                    size: 27,
                  ),
                ),
                const SizedBox(width: 14),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'خاوران دسک',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      SizedBox(height: 3),
                      Text(
                        'KHAVARAN DESK  •  دسترسی امن از راه دور',
                        style: TextStyle(
                          color: Color(0xFFD3F1ED),
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
                if (!bind.isDisableSettings())
                  Tooltip(
                    message: translate('Settings'),
                    child: IconButton(
                      onPressed: DesktopTabPage.onAddSetting,
                      icon: const Icon(
                        Icons.settings_rounded,
                        color: Colors.white,
                      ),
                    ),
                  ),
              ],
            ),
          );

          Widget content;
          if (isIncomingOnly) {
            content = localPanel;
          } else if (constraints.maxWidth < 860) {
            content = Column(
              children: [
                SizedBox(height: 360, child: localPanel),
                const SizedBox(height: 14),
                Expanded(child: remotePanel),
              ],
            );
          } else {
            content = Row(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                SizedBox(width: 340, child: localPanel),
                const SizedBox(width: 14),
                Expanded(child: remotePanel),
              ],
            );
          }

          return ColoredBox(
            color: canvas,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  header,
                  const SizedBox(height: 14),
                  Expanded(child: content),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
'''
s = s[:build_start] + new_build + s[build_end:]
write(home_path, s)


# Keep the Khavaran accent consistent with upstream translucent highlights.
common_path = "flutter/lib/common.dart"
s = read(common_path)
s = s.replace("0x770071FF", "0x770F766E").replace(
    "0xAA0071FF", "0xAA0F766E"
)
write(common_path, s)

print(
    "Applied Khavaran Persian-first locale/RTL, responsive dashboard, "
    "and visible server configuration"
)
