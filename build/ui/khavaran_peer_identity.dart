import 'package:flutter/material.dart';

/// Identity text never shares a Stack with status/platform decorations.
class KhavaranPeerIdentity extends StatelessWidget {
  const KhavaranPeerIdentity({super.key, required this.id, required this.alias,
    required this.online, required this.platform, required this.actions,
    this.details = '', this.compact = false});
  final String id, alias, details;
  final bool online, compact;
  final Widget platform, actions;

  TextDirection direction(String text) =>
      RegExp(r'[\u0590-\u08FF]').hasMatch(text)
          ? TextDirection.rtl : TextDirection.ltr;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: EdgeInsets.all(compact ? 10 : 18),
      child: Row(children: [
        Container(width: compact ? 36 : 46, height: compact ? 36 : 46,
          decoration: BoxDecoration(color: const Color(0xFF0F766E),
            borderRadius: BorderRadius.circular(12)),
          child: IconTheme(data: const IconThemeData(color: Colors.white), child: platform)),
        const SizedBox(width: 10),
        Expanded(child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (alias.isNotEmpty) Text(alias, textDirection: direction(alias),
              textAlign: Directionality.of(context) == TextDirection.rtl ? TextAlign.right : TextAlign.left, maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
            Row(children: [
              Container(key: const ValueKey('peer-status'), width: 7, height: 7,
                decoration: BoxDecoration(shape: BoxShape.circle,
                  color: online ? const Color(0xFF0F766E) : Colors.grey)),
              const SizedBox(width: 8),
              Expanded(child: Text(id, key: const ValueKey('peer-id'),
                textDirection: TextDirection.ltr, textAlign: Directionality.of(context) == TextDirection.rtl ? TextAlign.right : TextAlign.left,
                maxLines: 1, overflow: TextOverflow.ellipsis,
                style: theme.textTheme.bodyMedium?.copyWith(letterSpacing: 0.8))),
            ]),
            if (!compact && details.isNotEmpty) Text(details,
              textDirection: direction(details), maxLines: 1,
              overflow: TextOverflow.ellipsis, style: theme.textTheme.bodySmall),
          ],
        )),
        SizedBox(width: 48, child: actions),
      ]),
    );
  }
}
