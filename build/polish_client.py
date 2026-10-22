"""Product UI polish on the pinned, repaired client. No network-policy changes."""
from pathlib import Path
import os
import shutil

def edit(path, old, new):
 p=Path(path);s=p.read_text(encoding='utf-8')
 if s.count(old)!=1: raise RuntimeError(f'Patch point {path}: {old[:60]}')
 p.write_text(s.replace(old,new,1),encoding='utf-8')

for file in ('khavaran_notice.dart','khavaran_updates.dart'):
 shutil.copy2('build/ui/'+file, 'flutter/lib/desktop/widgets/'+file)
p=Path('flutter/lib/desktop/pages/desktop_home_page.dart');s=p.read_text(encoding='utf-8')
s="import '../widgets/khavaran_notice.dart';\nimport '../widgets/khavaran_updates.dart';\n"+s
start=s.index('    return Stack(',s.index('  Widget buildInstallCard('))
end=s.index('\n  @override\n  void initState()',start)
s=s[:start]+'''    return Padding(
      padding: EdgeInsets.only(top: marginTop),
      child: KhavaranNotice(
        title: translate(title), message: translate(content),
        action: translate(btnText), onAction: onPressed,
        help: help == null ? null : translate(help),
        onHelp: link == null ? null : () => launchUrl(Uri.parse(link)),
        onClose: closeButton == true ? closeCard : null,
      ),
    );
  }
''' +s[end:]
# GitHub run number belongs to the calling platform workflow, including reusable jobs.
number=int(os.environ.get('GITHUB_RUN_NUMBER','0'))
needle='          Obx(() => buildHelpCards(stateGlobal.updateUrl.value)),'
assert s.count(needle)==1
s=s.replace(needle,needle+f'''
          KhavaranUpdates(currentBuild: {number},
            prefix: isWindows ? 'client-windows-build-' : 'client-jetson-build-',
            openUrl: (url) => launchUrl(Uri.parse(url))),''')
p.write_text(s,encoding='utf-8')

# DynamicGridView's wrapping delegate lays the first card on the physical left.
# Flutter's native grid respects Directionality and fills the available width.
p='flutter/lib/common/widgets/peers_view.dart'
edit(p,'''DynamicGridView.builder(
                        gridDelegate: SliverGridDelegateWithWrapping(
                            mainAxisSpacing: space / 2,
                            crossAxisSpacing: space),''','''GridView.builder(
                        controller: _scrollController,
                        padding: const EdgeInsets.all(12),
                        gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
                            maxCrossAxisExtent: 380,
                            mainAxisExtent: 156,
                            mainAxisSpacing: 14,
                            crossAxisSpacing: 14),''')
p=Path(p);s=p.read_text(encoding='utf-8').replace("import 'package:dynamic_layouts/dynamic_layouts.dart';\n",'')
s=s.replace('width: 220, height: 140', 'width: 340, height: 156')
s=s.replace('width: 220, height: 72','width: 340, height: 88').replace('Container(height: 72,','Container(height: 88,')
p.write_text(s,encoding='utf-8')

p=Path('flutter/lib/common/widgets/peer_tab_page.dart');s=p.read_text(encoding='utf-8')
s=s.replace('              height: 32,','              height: 52,',1)
s=s.replace('physics: NeverScrollableScrollPhysics(),','physics: const ClampingScrollPhysics(),',1)
a=s.index('          final deco = BoxDecoration(',s.index('  Widget _createSwitchBar('))
b=s.index('          counter += 1;',a)
s=s[:a]+'''          final deco = BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: BorderRadius.circular(12));
          final decoBorder = BoxDecoration(
            color: const Color(0xFF0F766E),
            borderRadius: BorderRadius.circular(12));
''' +s[b:]
a=s.index('                        child: Icon(model.tabIcon(t), color: color)');b=s.index('\n                      ).paddingSymmetric',a)
s=s[:a]+'''                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
                        child: Row(mainAxisSize: MainAxisSize.min, children: [
                          Icon(const [Icons.history_rounded, Icons.star_outline_rounded,
                            Icons.radar_rounded, Icons.contacts_outlined,
                            Icons.devices_rounded][t],
                            size: 20, color: selected ? Colors.white : color),
                          if (selected) ...[
                            const SizedBox(width: 8),
                            ConstrainedBox(constraints: const BoxConstraints(maxWidth: 100),
                              child: Text(translate(model.tabTooltip(t)),
                                maxLines: 1, overflow: TextOverflow.ellipsis,
                                style: const TextStyle(color: Colors.white, fontSize: 12))),
                          ],
                        ]),''' +s[b:]
p.write_text(s,encoding='utf-8')

# Company navigation is distinct from the preserved upstream license notices.
p='flutter/lib/desktop/pages/install_page.dart'
edit(p,"'https://github.com/ehsanark/khavarandesk/blob/main/LICENSE'),\n                    child: const Text('مجوز نرم‌افزار و حقوق پدیدآورندگان'))", "'http://khavaranai.ir/'),\n                    child: const Text('شرکت خاوران — پدیدآورندگان'))")
print('Applied Khavaran notices, release checks, RTL grid and navigation chips')
