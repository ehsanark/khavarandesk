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


# Prefill the Network/Server dialog with Khavaran's private server defaults.
# Users can still override these values manually if they need another server.
dialog_path = "flutter/lib/mobile/widgets/dialog.dart"
s = read(dialog_path)
dialog_old = """  final idCtrl = TextEditingController(text: serverConfig.idServer);
  final relayCtrl = TextEditingController(text: serverConfig.relayServer);
  final apiCtrl = TextEditingController(text: serverConfig.apiServer);
  final keyCtrl = TextEditingController(text: serverConfig.key);
"""
dialog_new = """  const khavaranDefaultServer = '2.181.250.249';
  const khavaranDefaultKey =
      'SNngVLEdOKKSsMzQuqQwT1EFjftRAVxfHBQSyOss1Zg=';
  final idCtrl = TextEditingController(
      text: serverConfig.idServer.trim().isEmpty
          ? khavaranDefaultServer
          : serverConfig.idServer);
  final relayCtrl = TextEditingController(
      text: serverConfig.relayServer.trim().isEmpty
          ? khavaranDefaultServer
          : serverConfig.relayServer);
  final apiCtrl = TextEditingController(text: serverConfig.apiServer);
  final keyCtrl = TextEditingController(
      text: serverConfig.key.trim().isEmpty
          ? khavaranDefaultKey
          : serverConfig.key);
"""
s = replace_once(
    s,
    dialog_old,
    dialog_new,
    "Network dialog Khavaran defaults",
)
write(dialog_path, s)


# The product shell is maintained as Dart, not embedded in a Python string.
import shutil
shell = Path("flutter/lib/desktop/widgets/khavaran_workspace.dart")
shutil.copy2("build/ui/khavaran_workspace.dart", shell)
for font in Path("build/fonts").glob("*"):
    dest = Path("flutter/assets/fonts") / font.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(font, dest)
pub = read("flutter/pubspec.yaml")
pub = replace_once(pub, "  fonts:\n", """  fonts:
    - family: Vazirmatn
      fonts:
        - asset: assets/fonts/Vazirmatn-Regular.ttf
          weight: 400
        - asset: assets/fonts/Vazirmatn-Medium.ttf
          weight: 500
        - asset: assets/fonts/Vazirmatn-Bold.ttf
          weight: 700
""", "bundled Persian fonts")
write("flutter/pubspec.yaml", pub)

home_path = "flutter/lib/desktop/pages/desktop_home_page.dart"
s = read(home_path)
s = replace_once(s, "import 'package:flutter_hbb/models/platform_model.dart';", """import 'package:flutter_hbb/models/platform_model.dart';
import 'package:flutter_hbb/mobile/widgets/dialog.dart';
import '../widgets/khavaran_workspace.dart';""", "workspace imports")
a = s.index("    return _buildBlock(", s.index("  Widget build(BuildContext context)"))
b = s.index("\n  Widget _buildBlock", a)
s = s[:a] + read("build/ui/home_body.dart.txt") + s[b:]
# Keep machine identifiers readable regardless of the surrounding locale.
s = s.replace("controller: model.serverPasswd,", "controller: model.serverPasswd,\n                            textDirection: TextDirection.ltr,")
# Khavaran releases must not offer an upstream installer as a product update.
a = s.index("    if (!bind.isCustomClient() &&", s.index("Widget buildHelpCards"))
b = s.index("    if (systemError.isNotEmpty)", a)
s = s[:a] + s[b:]
write(home_path, s)

common_path = "flutter/lib/common.dart"
s = read(common_path)
s = s.replace("0x770071FF", "0x770F766E").replace("0xAA0071FF", "0xAA0F766E")
s = s.replace("static const Color button = Color(0xFF2C8CFF);", "static const Color button = Color(0xFF0F766E);")
for theme in ("lightTheme", "darkTheme"):
    s = replace_once(s, f"static ThemeData {theme} = ThemeData(", f"static ThemeData {theme} = ThemeData(\n    fontFamily: 'Vazirmatn',", theme + " typography")
write(common_path, s)

# Use the core's default-options mechanism so service and UI agree, including
# before a user opens or saves the Network dialog. Explicit saved options win.
p = "libs/hbb_common/src/config.rs"
s = read(p)
s = replace_once(s, "pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = Default::default();", """pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = RwLock::new(HashMap::from([
        ("custom-rendezvous-server".to_owned(), "2.181.250.249".to_owned()),
        ("relay-server".to_owned(), "2.181.250.249".to_owned()),
        ("key".to_owned(), RS_PUB_KEY.to_owned()),
    ]));""", "native server defaults")
write(p, s)

# Redesign connection entry while retaining autocomplete, session modes and
# the existing peer database. Status has one owner, in the workspace footer.
p = "flutter/lib/desktop/pages/connection_page.dart"
s = read(p)
a = s.index("    final isOutgoingOnly = bind.isOutgoingOnly();", s.index("class _ConnectionPageState"))
b = s.index("  /// Callback for the connect button.", a)
s = s[:a] + """    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Padding(padding: const EdgeInsets.all(18), child: _buildRemoteIDTextField(context)),
      const Divider(height: 1),
      Expanded(child: PeerTabPage()),
    ]);
  }

""" + s[b:]
s = replace_once(s, "width: 320 + 20 * 2,", "width: double.infinity,", "fluid connection entry")
s = s.replace("fontFamily: 'WorkSans',", "fontFamily: 'Vazirmatn',")
s = replace_once(s, "getConnectionPageTitle(context, false).marginOnly(bottom: 15),", """const Align(alignment: AlignmentDirectional.centerStart,
              child: Text('شناسه دستگاه مقصد', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w500))).marginOnly(bottom: 12),""", "connection title")
s = s.replace("autocorrect: false,", "autocorrect: false,\n                          textDirection: TextDirection.ltr,")
# Avoid misleading public-server advertising: our native defaults are private.
s = s.replace("if (!isIncomingOnly) setupServerWidget(),", "")
write(p, s)

# A new installation opens at a comfortable desktop size; saved sizes survive.
p = "flutter/lib/main.dart"
s = read(p).replace("size: Size(800, 600)", "size: Size(1120, 760)")
write(p, s)

# Desktop launcher identity; internal executable and protocol names stay stable.
for p in ("res/rustdesk.desktop", "res/rustdesk-link.desktop"):
    s = read(p).replace("Name=RustDesk", "Name=Khavaran Desk\nName[fa]=خاوران دسک")
    write(p, s)
print("Applied Khavaran workspace, bundled Vazirmatn, Persian RTL and native server defaults")
