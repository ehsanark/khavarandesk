import 'package:flutter/material.dart';

/// Product shell; all session, password and connection actions remain connected
/// to the native client. No simulated devices or network health indicators.
class KhavaranWorkspace extends StatelessWidget {
  const KhavaranWorkspace(
      {super.key,
      required this.local,
      required this.remote,
      required this.status,
      this.onSettings,
      this.onSecurity,
      this.onServer,
      this.incomingOnly = false,
      this.outgoingOnly = false});
  final Widget local, remote, status;
  final VoidCallback? onSettings, onSecurity, onServer;
  final bool incomingOnly, outgoingOnly;

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    final ink = dark ? const Color(0xFFE9EEF7) : const Color(0xFF17243B);
    final muted = dark ? const Color(0xFF9BAAC0) : const Color(0xFF68768C);
    final surface = dark ? const Color(0xFF172238) : Colors.white;
    final line = dark ? const Color(0xFF2B3950) : const Color(0xFFE5EAF1);

    Widget nav(IconData icon, String label, VoidCallback? action,
        {bool selected = false}) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
        child: Tooltip(
            message: label,
            child: Material(
              color: selected ? const Color(0xFF304969) : Colors.transparent,
              borderRadius: BorderRadius.circular(14),
              child: InkWell(
                onTap: action,
                borderRadius: BorderRadius.circular(14),
                child: SizedBox(
                    width: 60,
                    height: 62,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(icon,
                            color: selected
                                ? const Color(0xFF6BE0CB)
                                : const Color(0xFFBBC9DE),
                            size: 23),
                        const SizedBox(height: 5),
                        Text(label,
                            style: const TextStyle(
                                color: Color(0xFFE3EAF4), fontSize: 10))
                      ],
                    )),
              ),
            )),
      );
    }

    Widget card(String title, String subtitle, IconData icon, Widget body) {
      return Container(
        clipBehavior: Clip.antiAlias,
        decoration: BoxDecoration(
            color: surface,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: line)),
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Padding(
              padding: const EdgeInsets.all(20),
              child: Row(children: [
                Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                        color: dark
                            ? const Color(0xFF243D4C)
                            : const Color(0xFFEAF6F2),
                        borderRadius: BorderRadius.circular(12)),
                    child: Icon(icon,
                        size: 21,
                        color: dark
                            ? const Color(0xFF6BE0CB)
                            : const Color(0xFF087F72))),
                const SizedBox(width: 12),
                Expanded(
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                      Text(title,
                          style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              color: ink)),
                      const SizedBox(height: 4),
                      Text(subtitle,
                          style: TextStyle(fontSize: 11, color: muted)),
                    ])),
              ])),
          Divider(height: 1, color: line),
          Expanded(child: LayoutBuilder(builder: (context, bounds) {
            if (bounds.maxHeight < 360) {
              return SingleChildScrollView(
                  child: SizedBox(height: 360, child: body));
            }
            return body;
          })),
        ]),
      );
    }

    final localCard = card(
        'این دستگاه',
        'برای دریافت پشتیبانی، شناسه را به اشتراک بگذارید',
        Icons.desktop_windows_outlined,
        local);
    final remoteCard = card('فضای اتصال', 'یک شناسه، تا کنار هم کار کنیم',
        Icons.north_west_rounded, remote);

    return LayoutBuilder(builder: (context, box) {
      final compact = box.maxWidth < 920;
      return ColoredBox(
        color: dark ? const Color(0xFF0D1728) : const Color(0xFFF3F5F9),
        child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          if (box.maxWidth >= 600)
            Container(
                width: 80,
                color: const Color(0xFF14263F),
                child: Column(children: [
                  const SizedBox(height: 25),
                  Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                          color: const Color(0xFF53D5BF),
                          borderRadius: BorderRadius.circular(14)),
                      child: const Icon(Icons.hub_outlined,
                          color: Color(0xFF14263F), size: 27)),
                  const SizedBox(height: 25),
                  nav(Icons.grid_view_rounded, 'میز کار', null, selected: true),
                  if (onServer != null)
                    nav(Icons.dns_outlined, 'شبکه', onServer),
                  if (onSecurity != null)
                    nav(Icons.shield_outlined, 'امنیت', onSecurity),
                  const Spacer(),
                  if (onSettings != null)
                    nav(Icons.tune_rounded, 'تنظیمات', onSettings),
                  const SizedBox(height: 18),
                ])),
          Expanded(
              child: Padding(
                  padding: EdgeInsets.all(compact ? 16 : 26),
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Row(children: [
                          Expanded(
                              child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                Text('خاوران دسک',
                                    style: TextStyle(
                                        fontSize: 25,
                                        fontWeight: FontWeight.w700,
                                        color: ink)),
                                const SizedBox(height: 3),
                                Text('فاصله کمتر، همکاری بیشتر',
                                    style:
                                        TextStyle(fontSize: 12, color: muted)),
                              ])),
                          if (box.maxWidth >= 700)
                            Container(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 12, vertical: 8),
                                decoration: BoxDecoration(
                                    color: surface,
                                    border: Border.all(color: line),
                                    borderRadius: BorderRadius.circular(10)),
                                child: Text('KHAVARAN / WORKSPACE',
                                    textDirection: TextDirection.ltr,
                                    style: TextStyle(
                                        fontSize: 10,
                                        letterSpacing: 1.3,
                                        color: muted))),
                          if (box.maxWidth < 600 && onSettings != null)
                            IconButton(
                                tooltip: 'تنظیمات',
                                onPressed: onSettings,
                                icon: const Icon(Icons.tune_rounded)),
                        ]),
                        const SizedBox(height: 22),
                        Expanded(
                            child: incomingOnly
                                ? localCard
                                : outgoingOnly
                                    ? remoteCard
                                    : compact
                                        ? DefaultTabController(
                                            length: 2,
                                            child: Column(children: [
                                              TabBar(
                                                  labelColor: ink,
                                                  unselectedLabelColor: muted,
                                                  indicatorColor:
                                                      const Color(0xFF087F72),
                                                  tabs: const [
                                                    Tab(
                                                        text:
                                                            'اتصال به دستگاه'),
                                                    Tab(
                                                        text:
                                                            'دسترسی این دستگاه')
                                                  ]),
                                              const SizedBox(height: 12),
                                              Expanded(
                                                  child: TabBarView(children: [
                                                remoteCard,
                                                localCard
                                              ])),
                                            ]))
                                        : Row(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.stretch,
                                            children: [
                                                SizedBox(
                                                    width: 300,
                                                    child: localCard),
                                                const SizedBox(width: 18),
                                                Expanded(child: remoteCard),
                                              ])),
                        const SizedBox(height: 12),
                        SizedBox(height: 42, child: ClipRect(child: status)),
                      ]))),
        ]),
      );
    });
  }
}
