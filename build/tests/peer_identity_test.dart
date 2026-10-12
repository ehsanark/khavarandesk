import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:khavaran_ui/khavaran_peer_identity.dart';

void main() {
  for (final compact in [false, true]) {
    for (final dir in [TextDirection.rtl, TextDirection.ltr]) {
      testWidgets('peer identity compact=$compact direction=$dir', (tester) async {
        await tester.pumpWidget(MaterialApp(home: Scaffold(body: Center(
          child: Directionality(textDirection: dir, child: SizedBox(
            width: 220, height: compact ? 72 : 140,
            child: KhavaranPeerIdentity(id: '2 045 816 920',
              alias: 'رایانه شعبه مرکزی خاوران — واحد پشتیبانی',
              details: 'نام فارسی / Windows', online: true, compact: compact,
              platform: const Icon(Icons.desktop_windows),
              actions: IconButton(onPressed: () {}, icon: const Icon(Icons.more_vert))),
          )),
        ))));
        expect(tester.takeException(), isNull);
        final id = find.byKey(const ValueKey('peer-id'));
        final status = find.byKey(const ValueKey('peer-status'));
        expect(tester.getRect(id).overlaps(tester.getRect(status)), isFalse);
        expect(tester.widget<Text>(id).textDirection, TextDirection.ltr);
        expect(tester.widget<Text>(find.text('رایانه شعبه مرکزی خاوران — واحد پشتیبانی')).textDirection,
            TextDirection.rtl);
      });
    }
  }
}
