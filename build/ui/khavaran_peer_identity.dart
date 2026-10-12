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
      padding: EdgeInsets.all(compact ? 6 : 12),
      child: Row(children: [
        SizedBox(width: compact ? 30 : 38, child: platform),
        const SizedBox(width: 10),
        Expanded(child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (alias.isNotEmpty) Text(alias, textDirection: direction(alias),
              textAlign: TextAlign.start, maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: theme.textTheme.titleSmall),
            Row(children: [
              Container(key: const ValueKey('peer-status'), width: 7, height: 7,
                decoration: BoxDecoration(shape: BoxShape.circle,
                  color: online ? const Color(0xFF0F766E) : Colors.grey)),
              const SizedBox(width: 8),
              Expanded(child: Text(id, key: const ValueKey('peer-id'),
                textDirection: TextDirection.ltr, textAlign: TextAlign.start,
                maxLines: 1, overflow: TextOverflow.ellipsis,
                style: theme.textTheme.bodySmall)),
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
