import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app/app_state.dart';
import '../widgets/calm_scaffold.dart';

class ParentDashboardScreen extends StatefulWidget {
  const ParentDashboardScreen({super.key});

  @override
  State<ParentDashboardScreen> createState() => _ParentDashboardScreenState();
}

class _ParentDashboardScreenState extends State<ParentDashboardScreen> {
  late Future<Map<String, dynamic>> _reportFuture;

  @override
  void initState() {
    super.initState();
    _reportFuture = _loadReport();
  }

  Future<Map<String, dynamic>> _loadReport() async {
    final appState = context.read<AppState>();
    final studentId = await appState.ensureRemoteProfile();
    return appState.api.getParentsReport(studentId);
  }

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Painel dos pais',
      child: FutureBuilder<Map<String, dynamic>>(
        future: _reportFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            final profile = context.watch<AppState>().profile;
            return ListView(
              padding: const EdgeInsets.all(20),
              children: [
                _card('Relatorio indisponivel', 'Nao consegui conectar com o backend agora.\n\n${snapshot.error}'),
                _card('Materias cadastradas', profile.difficultSubjects),
                _card('Estrategias que ajudam', profile.helpfulStrategies),
                const SizedBox(height: 10),
                const Text(
                  'Privacidade: mantenha o minimo de dados necessario e apague o historico quando desejar.',
                  textAlign: TextAlign.center,
                ),
              ],
            );
          }

          final report = snapshot.data ?? const {};
          final subjects = (report['subjects_studied'] as List<dynamic>? ?? const [])
              .map((item) => item.toString())
              .join(', ');
          final achievements = (report['recent_achievements'] as List<dynamic>? ?? const [])
              .map((item) => item is Map<String, dynamic> ? item['title']?.toString() : item.toString())
              .where((item) => item != null && item.trim().isNotEmpty)
              .cast<String>()
              .join(', ');

          return RefreshIndicator(
            onRefresh: () async {
              setState(() {
                _reportFuture = _loadReport();
              });
              await _reportFuture;
            },
            child: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                _card('Aluna', report['student_name']?.toString() ?? 'Perfil sem nome'),
                _card('Sessoes na semana', '${report['week_sessions'] ?? 0}'),
                _card('Tempo de estudo', '${report['total_study_minutes'] ?? 0} minutos'),
                _card('Materias estudadas', subjects.isEmpty ? 'Ainda sem sessoes registradas.' : subjects),
                _card('Momentos de travamento', '${report['stuck_moments'] ?? 0}'),
                _card('Microvitorias recentes', achievements.isEmpty ? 'Ainda sem microvitorias registradas nesta semana.' : achievements),
                _card('Observacao pedagogica', report['pedagogical_note']?.toString() ?? 'Sem observacao no momento.'),
                const SizedBox(height: 10),
                const Text(
                  'Privacidade: mantenha o minimo de dados necessario e apague o historico quando desejar.',
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _card(String title, String text) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            Text(text, style: const TextStyle(fontSize: 15, height: 1.35)),
          ],
        ),
      ),
    );
  }
}
