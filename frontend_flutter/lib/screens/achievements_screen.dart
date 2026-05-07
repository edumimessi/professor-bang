import 'package:flutter/material.dart';

import '../widgets/calm_scaffold.dart';

class AchievementsScreen extends StatelessWidget {
  const AchievementsScreen({super.key});

  static const achievements = [
    ['Começou sozinha', 'Iniciou uma atividade sem pressão.'],
    ['Tentou mesmo com dificuldade', 'Manteve o esforço quando apareceu um desafio.'],
    ['Pediu pista', 'Usou uma estratégia de autonomia.'],
    ['Terminou uma etapa', 'Concluiu uma parte pequena da tarefa.'],
    ['Fez pausa e voltou', 'Regulou a ansiedade e retomou com calma.'],
  ];

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Microvitórias',
      child: ListView.builder(
        padding: const EdgeInsets.all(20),
        itemCount: achievements.length,
        itemBuilder: (context, index) {
          final item = achievements[index];
          return Card(
            child: ListTile(
              leading: const Icon(Icons.stars),
              title: Text(item[0], style: const TextStyle(fontWeight: FontWeight.w800)),
              subtitle: Text(item[1]),
            ),
          );
        },
      ),
    );
  }
}
