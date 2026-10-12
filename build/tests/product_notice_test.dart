import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:khavaran_ui/khavaran_notice.dart';
import 'package:khavaran_ui/khavaran_updates.dart';

void main() {
  test('updates select only newer Khavaran platform releases', () {
    Map<String, dynamic> release(String tag, {String? url}) => {
      'tag_name': tag, 'html_url': url ?? 'https://github.com/ehsanark/khavarandesk/releases/tag/$tag',
      'assets': [{'name': 'client.exe'}], 'draft': false,
    };
    final releases = [release('client-jetson-build-90'),
      release('client-windows-build-17'), release('client-windows-build-19'),
      release('client-windows-build-18'),
      release('client-windows-build-99', url: 'https://example.com/other.exe')];
    expect(khavaranLatestRelease(releases, 'client-windows-build-', 17)?['tag_name'],
      'client-windows-build-19');
    expect(khavaranLatestRelease(releases, 'client-windows-build-', 19), isNull);
  });
  testWidgets('notice fits narrow RTL pane and retains update action', (tester) async {
    var actions = 0;
    await tester.pumpWidget(MaterialApp(home: Directionality(
      textDirection: TextDirection.rtl, child: Scaffold(body: Center(
        child: SizedBox(width: 250, child: KhavaranNotice(
          title: 'به‌روزرسانی خاوران دسک', message: 'نسخه جدید برای تیم شما آماده است.',
          action: 'دریافت نسخه جدید', onAction: () => actions++)),
      )))));
    expect(tester.takeException(), isNull);
    await tester.tap(find.text('دریافت نسخه جدید'));
    expect(actions, 1);
  });
}
