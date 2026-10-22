import 'package:flutter/material.dart';

class KhavaranNotice extends StatelessWidget {
  const KhavaranNotice({super.key, required this.title, required this.message,
    this.action = '', this.onAction, this.help, this.onHelp, this.onClose});
  final String title, message, action;
  final VoidCallback? onAction, onHelp, onClose;
  final String? help;
  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: dark ? const Color(0xFF183B3B) : const Color(0xFFF0FAF7),
        border: Border.all(color: const Color(0xFFB5DCD3)),
        borderRadius: BorderRadius.circular(18)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Row(children: [
          const Icon(Icons.system_update_alt_rounded, color: Color(0xFF0F766E), size: 24),
          const SizedBox(width: 10),
          Expanded(child: Text(title.isEmpty ? 'خاوران دسک' : title,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700))),
          if (onClose != null) IconButton(onPressed: onClose,
            icon: const Icon(Icons.close_rounded, size: 18)),
        ]),
        if (message.isNotEmpty) ...[
          const SizedBox(height: 12),
          Text(message, style: const TextStyle(fontSize: 13, height: 1.8)),
        ],
        if (action.isNotEmpty) ...[
          const SizedBox(height: 16),
          FilledButton(onPressed: onAction,
            style: FilledButton.styleFrom(backgroundColor: const Color(0xFF0F766E),
              foregroundColor: Colors.white, padding: const EdgeInsets.all(14)),
            child: Text(action)),
        ],
        if (help != null && onHelp != null)
          TextButton(onPressed: onHelp, child: Text(help!)),
      ]),
    );
  }
}
