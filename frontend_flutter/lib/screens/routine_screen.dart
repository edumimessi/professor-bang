import 'package:flutter/material.dart';

import '../widgets/calm_scaffold.dart';

class RoutineScreen extends StatefulWidget {
  const RoutineScreen({super.key});

  @override
  State<RoutineScreen> createState() => _RoutineScreenState();
}

class _RoutineScreenState extends State<RoutineScreen> {
  final List<_RoutineItem> tasks = [
    _RoutineItem('Pegar caderno'),
    _RoutineItem('Pegar lápis'),
    _RoutineItem('Separar água'),
    _RoutineItem('Abrir tarefa'),
    _RoutineItem('Estudar por 10 minutos'),
    _RoutineItem('Fazer pausa'),
    _RoutineItem('Marcar concluído'),
  ];

  @override
  Widget build(BuildContext context) {
    final done = tasks.where((task) => task.done).length;
    return CalmScaffold(
      title: 'Rotina de estudo',
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Text(
                'Faça uma coisa por vez. Concluído: $done de ${tasks.length}.',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
              ),
            ),
          ),
          const SizedBox(height: 12),
          for (final task in tasks)
            Card(
              child: CheckboxListTile(
                value: task.done,
                onChanged: (value) => setState(() => task.done = value ?? false),
                title: Text(task.title, style: const TextStyle(fontSize: 17)),
                controlAffinity: ListTileControlAffinity.leading,
              ),
            ),
        ],
      ),
    );
  }
}

class _RoutineItem {
  _RoutineItem(this.title);
  final String title;
  bool done = false;
}
