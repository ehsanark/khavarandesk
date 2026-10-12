import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:khavaran_ui/khavaran_workspace.dart';

void main() {
  setUpAll(() async {
    final loader = FontLoader('Vazirmatn');
    for (final weight in ['Regular', 'Medium', 'Bold']) {
      loader.addFont(rootBundle.load('fonts/Vazirmatn-$weight.ttf'));
    }
    await loader.load();
  });
  for (final size in [
    const Size(1120, 760),
    const Size(800, 600),
    const Size(600, 480)
  ]) {
    for (final dark in [false, true]) {
      testWidgets('RTL workspace ${size.width} dark=$dark', (tester) async {
        tester.view.physicalSize = size;
        tester.view.devicePixelRatio = 1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        var settings = 0;
        final theme = ThemeData(
            brightness: dark ? Brightness.dark : Brightness.light,
            fontFamily: 'Vazirmatn');
        await tester.pumpWidget(MaterialApp(
            theme: theme,
            home: Directionality(
                textDirection: TextDirection.rtl,
                child: Scaffold(
                    body: RepaintBoundary(
                        key: const Key('workspace'),
                        child: KhavaranWorkspace(
                          onSettings: () => settings++,
                          onSecurity: () {},
                          onServer: () {},
                          status: const Align(
                              alignment: AlignmentDirectional.centerStart,
                              child: Text(
                                  'پیش‌نمایش رابط • اتصال زنده در این آزمون وجود ندارد')),
                          local: const Padding(
                              padding: EdgeInsets.all(24),
                              child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    Text('شناسه شما'),
                                    SizedBox(height: 16),
                                    Text('2 045 816 920',
                                        textDirection: TextDirection.ltr,
                                        style: TextStyle(
                                            fontSize: 26,
                                            fontWeight: FontWeight.bold)),
                                    SizedBox(height: 28),
                                    Text('رمز یک‌بارمصرف'),
                                    SizedBox(height: 12),
                                    Text('••••••',
                                        style: TextStyle(fontSize: 24)),
                                    SizedBox(height: 30),
                                    Divider(),
                                    SizedBox(height: 20),
                                    Text('سرور اتصال'),
                                    SizedBox(height: 12),
                                    Text('2.181.250.249',
                                        textDirection: TextDirection.ltr),
                                  ])),
                          remote: Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    const Text('شناسه دستگاه مقصد'),
                                    const SizedBox(height: 14),
                                    const TextField(
                                        textDirection: TextDirection.ltr,
                                        decoration: InputDecoration(
                                            hintText: 'شناسه دستگاه',
                                            border: OutlineInputBorder())),
                                    const SizedBox(height: 14),
                                    FilledButton(
                                        onPressed: () {},
                                        child: const Text('اتصال')),
                                    const SizedBox(height: 30),
                                    const Divider(),
                                    const SizedBox(height: 30),
                                    const Icon(Icons.devices_outlined,
                                        size: 40, color: Colors.grey),
                                    const SizedBox(height: 16),
                                    const Text('هنوز دستگاهی اضافه نشده است',
                                        textAlign: TextAlign.center),
                                  ])),
                        ))))));
        await tester.pumpAndSettle();
        expect(tester.takeException(), isNull);
        expect(find.text('خاوران دسک'), findsOneWidget);
        await tester.tap(find.byTooltip('تنظیمات'));
        expect(settings, 1);
        await tester.pumpAndSettle();
        if (size.width == 1120) {
          await expectLater(
              find.byKey(const Key('workspace')),
              matchesGoldenFile(
                  'screenshots/workspace-${dark ? 'dark' : 'light'}.png'));
        } else {
          await tester.tap(find.text('دسترسی این دستگاه'));
          await tester.pumpAndSettle();
          expect(find.text('شناسه شما').hitTestable(), findsOneWidget);
          expect(tester.takeException(), isNull);
        }
      });
    }
  }
}
