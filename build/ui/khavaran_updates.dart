import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'khavaran_notice.dart';

/// Compare product build numbers, not RustDesk's upstream version string.
Map<String, dynamic>? khavaranLatestRelease(List<dynamic> releases, String prefix, int current) {
  Map<String, dynamic>? latest;
  var newest = current;
  for (final item in releases) {
    if (item is! Map<String, dynamic> || item['draft'] == true) continue;
    final tag = item['tag_name']?.toString() ?? '';
    if (!tag.startsWith(prefix)) continue;
    final number = int.tryParse(tag.substring(prefix.length));
    if (number == null || number <= newest) continue;
    final url = item['html_url']?.toString() ?? '';
    if (!url.startsWith('https://github.com/ehsanark/khavarandesk/releases/tag/')) continue;
    if (item['assets'] is! List || (item['assets'] as List).isEmpty) continue;
    newest = number;
    latest = item;
  }
  return latest;
}

class KhavaranUpdates extends StatefulWidget {
  const KhavaranUpdates({super.key, required this.currentBuild,
    required this.prefix, required this.openUrl});
  final int currentBuild;
  final String prefix;
  final void Function(String) openUrl;
  @override
  State<KhavaranUpdates> createState() => _KhavaranUpdatesState();
}
class _KhavaranUpdatesState extends State<KhavaranUpdates> {
  bool busy = false;
  String message = '';
  Map<String, dynamic>? release;
  @override
  void initState() { super.initState(); check(); }
  Future<void> check() async {
    if (busy) return;
    setState(() { busy = true; message = ''; });
    final client = HttpClient()..connectionTimeout = const Duration(seconds: 10);
    try {
      final request = await client.getUrl(Uri.parse(
        'https://api.github.com/repos/ehsanark/khavarandesk/releases?per_page=100'));
      request.headers.set('User-Agent', 'KhavaranDesk');
      request.headers.set('Accept', 'application/vnd.github+json');
      final response = await request.close().timeout(const Duration(seconds: 15));
      if (response.statusCode != 200) throw HttpException('HTTP ${response.statusCode}');
      final raw = await response.transform(utf8.decoder).join().timeout(const Duration(seconds: 15));
      final latest = khavaranLatestRelease(jsonDecode(raw) as List<dynamic>, widget.prefix, widget.currentBuild);
      if (mounted) setState(() { release = latest;
        message = latest == null ? 'نسخه جدیدتری منتشر نشده است.' : 'نسخه جدید خاوران دسک آماده دریافت است.'; });
    } catch (_) {
      if (mounted) setState(() { message = 'بررسی نسخه ممکن نشد؛ دوباره تلاش کنید.'; });
    } finally {
      client.close(force: true);
      if (mounted) setState(() { busy = false; });
    }
  }
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.all(12),
    child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      if (release != null) KhavaranNotice(title: 'به‌روزرسانی خاوران دسک',
        message: message, action: 'دریافت نسخه جدید',
        onAction: () => widget.openUrl(release!['html_url'] as String))
      else if (message.isNotEmpty) Text(message, style: const TextStyle(fontSize: 12)),
      TextButton.icon(onPressed: busy ? null : check,
        icon: const Icon(Icons.refresh_rounded, size: 18),
        label: Text(busy ? 'در حال بررسی…' : 'بررسی به‌روزرسانی خاوران')),
    ]),
  );
}
