"""Apply the Khavaran desktop dashboard to the pinned, branded source."""
from pathlib import Path

p = Path('flutter/lib/desktop/pages/desktop_home_page.dart')
s = p.read_text(encoding='utf-8')
start = s.index('    return _buildBlock(', s.index('  Widget build(BuildContext context)'))
end = s.index('\n  Widget _buildBlock', start)
s = s[:start] + '''    final isOutgoingOnly = bind.isOutgoingOnly();
    return _buildBlock(child: LayoutBuilder(builder: (context, constraints) {
      final dark = Theme.of(context).brightness == Brightness.dark;
      final cardColor = dark ? const Color(0xFF182435) : Colors.white;
      Widget card(Widget child) => Container(
        clipBehavior: Clip.antiAlias,
        decoration: BoxDecoration(
          color: cardColor,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: const Color(0xFF0F766E).withOpacity(.18)),
        ),
        child: child,
      );
      final local = card(SingleChildScrollView(
        controller: _leftPaneScrollController,
        child: Column(key: _childKey, crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(padding: const EdgeInsets.all(20), child: Row(children: [
              const Icon(Icons.computer_rounded, color: MyTheme.accent),
              const SizedBox(width: 10),
              Expanded(child: Text(translate('Your Desktop'),
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700))),
            ])),
            if (!isOutgoingOnly) buildPresetPasswordWarning(),
            if (!isOutgoingOnly) buildIDBoard(context),
            if (!isOutgoingOnly) buildPasswordBoard(context),
            Padding(padding: const EdgeInsets.all(20), child: Text(
              translate('desk_tip'), style: Theme.of(context).textTheme.bodySmall)),
            const Divider(height: 1),
            Padding(padding: const EdgeInsets.all(16), child: OnlineStatusWidget()),
            if (!bind.isDisableSettings()) Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: OutlinedButton.icon(
                onPressed: () => DesktopSettingPage.switch2page(SettingsTabKey.network),
                icon: const Icon(Icons.dns_outlined),
                label: const Text('Server settings / تنظیمات سرور'),
              )),
            Obx(() => buildHelpCards(stateGlobal.updateUrl.value)),
          ],
        ),
      ));
      final remote = card(buildRightPane(context));
      return ColoredBox(
        color: dark ? const Color(0xFF0C1422) : const Color(0xFFF0F5F5),
        child: Padding(padding: const EdgeInsets.all(16), child: Column(children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFF102C3A), Color(0xFF0F766E)]),
              borderRadius: BorderRadius.circular(20)),
            child: Row(children: [
              const Icon(Icons.hub_rounded, color: Color(0xFF5EEAD4), size: 34),
              const SizedBox(width: 14),
              const Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('KHAVARAN DESK', style: TextStyle(color: Colors.white,
                    fontSize: 22, fontWeight: FontWeight.w800, letterSpacing: 1.5)),
                  SizedBox(height: 4),
                  Text('خاوران دسک | فضای کار از راه دور',
                    style: TextStyle(color: Color(0xFFBFE8E3), fontSize: 12)),
                ])),
              if (!bind.isDisableSettings()) IconButton(
                tooltip: translate('Settings'),
                onPressed: DesktopTabPage.onAddSetting,
                icon: const Icon(Icons.tune_rounded, color: Colors.white)),
            ])),
          const SizedBox(height: 16),
          Expanded(child: isIncomingOnly ? local : constraints.maxWidth < 720
            ? Column(children: [SizedBox(height: 245, child: local),
                const SizedBox(height: 12), Expanded(child: remote)])
            : Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                Expanded(child: remote), const SizedBox(width: 16),
                SizedBox(width: 285, child: local),
              ])),
        ])),
      );
    }));
  }
''' + s[end:]
p.write_text(s, encoding='utf-8')

# Carry the same accent through translucent highlights.
p = Path('flutter/lib/common.dart')
s = p.read_text(encoding='utf-8').replace('0x770071FF', '0x770F766E').replace('0xAA0071FF', '0xAA0F766E')
p.write_text(s, encoding='utf-8')
print('Applied Khavaran dashboard and visible server-settings entry point')
