"""Guarded fixes applied after network.patch to the pinned client source."""
from pathlib import Path
import shutil

def replace(path, old, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if s.count(old) != 1:
        raise RuntimeError(f'Unexpected patch point in {path}: {old[:70]}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')

def replace_body(path, signature, body):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    start = s.index(signature) + len(signature)
    end, depth = start, 1
    while depth:
        if s[end] == '{': depth += 1
        elif s[end] == '}': depth -= 1
        end += 1
    p.write_text(s[:start] + '\n' + body + '\n  }' + s[end:], encoding='utf-8')

# An older installed service must not redirect the new UI to an old server.
replace_body('src/common.rs',
    'async fn get_rendezvous_server_(ms_timeout: u64) -> (String, Vec<String>) {',
    '''    let _ = ms_timeout;
    (Config::get_rendezvous_server(), Config::get_rendezvous_servers())''')
# Both manual and background update callers use this entry point.
replace('src/common.rs',
    'pub async fn do_check_software_update() -> hbb_common::ResultType<()> {',
    '''pub async fn do_check_software_update() -> hbb_common::ResultType<()> {
    if is_custom_client() {
        SOFTWARE_UPDATE_URL.lock().unwrap().clear();
        return Ok(());
    }''')

shutil.copy2('build/ui/khavaran_peer_identity.dart',
             'flutter/lib/common/widgets/khavaran_peer_identity.dart')
p = 'flutter/lib/common/widgets/peer_card.dart'
replace(p, "import 'dart:math' as math;",
        "import 'dart:math' as math;\nimport 'khavaran_peer_identity.dart';")
replace_body(p, '  makeChild(bool isPortrait, Peer peer) {', '''    return KhavaranPeerIdentity(
      id: formatID(peer.id), alias: peer.alias, online: peer.online,
      compact: true,
      platform: getPlatformImage(peer.platform, size: 26),
      actions: isPortrait ? checkBoxOrActionMorePortrait(peer)
          : checkBoxOrActionMoreLandscape(peer, isTile: true),
    );''')
# Keep the existing card selection, context menu, key badge and tag indicators.
s = Path(p).read_text(encoding='utf-8')
a = s.index('    final child = Card(', s.index('  Widget _buildPeerCard('))
b = s.index('\n    final colors = ', a)
s = s[:a] + '''    final child = Obx(() => Container(
      foregroundDecoration: deco.value,
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(_cardRadius),
        border: Border.all(color: Theme.of(context).dividerColor),
      ),
      padding: const EdgeInsets.only(top: 12),
      child: KhavaranPeerIdentity(
        id: formatID(peer.id), alias: peer.alias, online: peer.online,
        details: _showNote(peer) ? peer.note : name,
        platform: getPlatformImage(peer.platform, size: 30),
        actions: checkBoxOrActionMoreLandscape(peer, isTile: false),
      ),
    ));
''' + s[b:]
# Platform/status elements have their own layout space; direction-aware padding.
s = s.replace('EdgeInsets.fromLTRB(0, 4, rightPadding, 4)',
              'EdgeInsetsDirectional.fromSTEB(0, 4, rightPadding, 4)')
Path(p).write_text(s, encoding='utf-8')
p = Path('flutter/lib/common/widgets/peers_view.dart')
s = p.read_text(encoding='utf-8').replace('Container(height: 45,', 'Container(height: 72,')
s = s.replace('width: 220, height: 42,', 'width: 220, height: 72,')
p.write_text(s, encoding='utf-8')

# Brand the existing installation/upgrade cards without changing native actions.
p = Path('flutter/lib/desktop/pages/desktop_home_page.dart')
s = p.read_text(encoding='utf-8')
s = s.replace('"", bind.isOutgoingOnly() ? "" : "install_tip", "Install",',
    '"خاوران دسک", "برای دسترسی پایدار، خاوران دسک را روی این دستگاه نصب کنید.", "نصب خاوران دسک",')
s = s.replace('"Status", "Your installation is lower version.", "Click to upgrade",',
    '"به‌روزرسانی خاوران دسک", "نسخه نصب‌شده قدیمی‌تر از نسخه در حال اجراست.", "به‌روزرسانی نصب",')
p.write_text(s, encoding='utf-8')
# Installation body: keep native install options/callbacks, replace its layout.
replace_body('flutter/lib/desktop/pages/install_page.dart',
    '  Widget build(BuildContext context) {\n    final double em = 13;',
    '''    return Scaffold(
      backgroundColor: const Color(0xFFF2F5FA),
      body: Directionality(textDirection: TextDirection.rtl,
        child: Center(child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 640),
            child: Card(child: Padding(padding: const EdgeInsets.all(24),
              child: Column(crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(Icons.desktop_windows_rounded, size: 48,
                    color: Color(0xFF0F766E)),
                  const SizedBox(height: 16),
                  const Text('نصب خاوران دسک', textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 12),
                  const Text('دسترسی امن تیم شما به دستگاه‌های سازمان',
                    textAlign: TextAlign.center),
                  const SizedBox(height: 24),
                  const Text('مسیر نصب'),
                  TextField(controller: controller, readOnly: true,
                    textDirection: TextDirection.ltr),
                  Obx(() => TextButton.icon(
                    onPressed: btnEnabled.value ? selectInstallPath : null,
                    icon: const Icon(Icons.folder_outlined),
                    label: const Text('انتخاب پوشه نصب'))),
                  Option(startmenu, label: 'Create start menu shortcuts'),
                  Option(desktopicon, label: 'Create desktop icon'),
                  Option(printer, label: 'Install {$appName} Printer'),
                  const SizedBox(height: 16),
                  TextButton(onPressed: () => launchUrlString(
                    'https://github.com/ehsanark/khavarandesk/blob/main/LICENSE'),
                    child: const Text('مجوز نرم‌افزار و حقوق پدیدآورندگان')),
                  Obx(() => showProgress.value
                    ? const LinearProgressIndicator() : const SizedBox.shrink()),
                  const SizedBox(height: 16),
                  Wrap(spacing: 12, runSpacing: 12, children: [
                    Obx(() => FilledButton.icon(
                      onPressed: btnEnabled.value ? install : null,
                      icon: const Icon(Icons.download_rounded),
                      label: const Text('تأیید و نصب خاوران دسک'))),
                    Obx(() => TextButton(
                      onPressed: btnEnabled.value ? () => windowManager.close() : null,
                      child: const Text('انصراف'))),
                    if (!bind.installShowRunWithoutInstall())
                      Obx(() => TextButton(
                        onPressed: btnEnabled.value
                          ? () => bind.installRunWithoutInstall() : null,
                        child: const Text('اجرای موقت'))),
                  ]),
                ],
              ),
            )),
          ),
        )),
      ),
    );''')
print('Applied managed routing, RTL peer layout and Khavaran installer fixes')

replace('flutter/lib/desktop/pages/desktop_setting_page.dart',
        '      if (showAutoUpdate)\n',
        '      if (showAutoUpdate && !bind.isCustomClient())\n')
replace('src/lang/fa.rs',
        '("ID does not exist", "شناسه وجود ندارد"),',
        '("ID does not exist", "شناسه مقصد روی سرور اتصال یافت نشد. خاوران دسک را در مقصد باز کنید، شناسه فعلی آن را دوباره وارد کنید و مطمئن شوید هر دو دستگاه از یک سرور استفاده می‌کنند."),')
# Use the same product typography and spacing in installation option rows.
p = Path('flutter/lib/desktop/pages/install_page.dart')
s = p.read_text(encoding='utf-8').replace('    final double em = 13;\n', '')
s = s.replace(').marginOnly(right: 8),', ').paddingOnly(left: 8),')
p.write_text(s, encoding='utf-8')
