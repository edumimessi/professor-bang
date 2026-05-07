import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app/app_state.dart';
import '../widgets/calm_scaffold.dart';

class ParentDashboardScreen extends StatelessWidget {
  const ParentDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final profile = context.watch<AppState>().profile;
    return CalmScaffold(
      title: 'Painel dos pais',
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _card('Matérias estudadas', profile.difficultSubjects),
          _card('Tempo de estudo', 'MVP local: registrar duração real será a próxima melhoria.'),
          _card('Momentos de travamento', 'Observar frases como “não sei”, pedidos repetidos e ansiedade.'),
          _card('Estratégias que funcionaram', profile.helpfulStrategies),
          _card('Evolução semanal', 'Sem ranking. Acompanhar microvitórias e retorno após pausas.'),
          _card('Observações pedagógicas', 'Usar frases curtas, uma pergunta por vez e exemplos concretos.'),
          const SizedBox(height: 10),
          const Text(
            'Privacidade: mantenha o mínimo de dados necessário e apague o histórico quando desejar.',
            textAlign: TextAlign.center,
          ),
        ],
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
