import 'package:flutter/material.dart';

import '../widgets/big_menu_button.dart';
import '../widgets/calm_scaffold.dart';
import 'chat_screen.dart';

class StudyModesScreen extends StatelessWidget {
  const StudyModesScreen({super.key});

  static const modes = [
    'Me explica devagar',
    'Me ajuda com a tarefa',
    'Me dá um exemplo',
    'Pode repetir?',
    'Estou travada',
    'Treinar para prova',
    'Rotina de estudo',
    'Pausa para respirar',
  ];

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Modos de estudo',
      child: ListView.separated(
        padding: const EdgeInsets.all(20),
        itemCount: modes.length,
        separatorBuilder: (_, __) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final mode = modes[index];
          return BigMenuButton(
            label: mode,
            icon: _iconFor(mode),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ChatScreen(initialMode: mode))),
          );
        },
      ),
    );
  }

  IconData _iconFor(String mode) {
    if (mode.contains('travada')) return Icons.volunteer_activism;
    if (mode.contains('Rotina')) return Icons.checklist;
    if (mode.contains('respirar')) return Icons.self_improvement;
    if (mode.contains('prova')) return Icons.quiz;
    return Icons.auto_stories;
  }
}
