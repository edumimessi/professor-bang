import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app/app_state.dart';
import '../widgets/calm_scaffold.dart';

class RoutineScreen extends StatefulWidget {
  const RoutineScreen({super.key});

  @override
  State<RoutineScreen> createState() => _RoutineScreenState();
}

class _RoutineScreenState extends State<RoutineScreen> {
  late Future<List<Map<String, dynamic>>> _tasksFuture;

  @override
  void initState() {
    super.initState();
    _tasksFuture = _loadTasks();
  }

  Future<List<Map<String, dynamic>>> _loadTasks() async {
    final appState = context.read<AppState>();
    final studentId = await appState.ensureRemoteProfile();
    return appState.api.getTodayRoutine(studentId);
  }

  Future<void> _toggleTask(Map<String, dynamic> task, bool isCompleted) async {
    final appState = context.read<AppState>();
    await appState.api.toggleRoutineTask(task['id'] as int, isCompleted);
    if (!mounted) return;
    setState(() {
      _tasksFuture = _loadTasks();
    });
  }

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Rotina de estudo',
      child: FutureBuilder<List<Map<String, dynamic>>>(
        future: _tasksFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Padding(
              padding: const EdgeInsets.all(20),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Text(
                    'Nao consegui carregar a rotina do backend agora.\n\n${snapshot.error}',
                    style: const TextStyle(fontSize: 15, height: 1.35),
                  ),
                ),
              ),
            );
          }

          final tasks = snapshot.data ?? const [];
          final done = tasks.where((task) => task['is_completed'] == true).length;

          return RefreshIndicator(
            onRefresh: () async {
              setState(() {
                _tasksFuture = _loadTasks();
              });
              await _tasksFuture;
            },
            child: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Text(
                      'Faca uma coisa por vez. Concluido: $done de ${tasks.length}.',
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                for (final task in tasks)
                  Card(
                    child: CheckboxListTile(
                      value: task['is_completed'] == true,
                      onChanged: (value) => _toggleTask(task, value ?? false),
                      title: Text(
                        task['title']?.toString() ?? 'Tarefa',
                        style: const TextStyle(fontSize: 17),
                      ),
                      controlAffinity: ListTileControlAffinity.leading,
                    ),
                  ),
              ],
            ),
          );
        },
      ),
    );
  }
}
