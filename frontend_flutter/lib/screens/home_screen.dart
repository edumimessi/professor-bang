import 'package:flutter/material.dart';

import '../app/app_theme.dart';
import '../widgets/big_menu_button.dart';
import '../widgets/calm_scaffold.dart';
import 'achievements_screen.dart';
import 'chat_screen.dart';
import 'parent_dashboard_screen.dart';
import 'profile_screen.dart';
import 'routine_screen.dart';
import 'study_modes_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return CalmScaffold(
      title: 'Professor Bang',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 20),
        children: [
          _HeroPanel(
            onStart: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const StudyModesScreen()),
            ),
          ),
          const SizedBox(height: 16),
          const _SectionTitle('Acoes principais'),
          const SizedBox(height: 8),
          BigMenuButton(
            label: 'Chat pedagogico',
            subtitle: 'Ajuda passo a passo, pistas e modo apoio.',
            icon: Icons.chat_bubble_outline,
            accentColor: AppTheme.calmBlue,
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ChatScreen(initialMode: 'Me explica devagar')),
            ),
          ),
          const SizedBox(height: 10),
          BigMenuButton(
            label: 'Rotina de estudo',
            subtitle: 'Checklist curto para organizar o dia.',
            icon: Icons.checklist,
            accentColor: AppTheme.moss,
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const RoutineScreen()),
            ),
          ),
          const SizedBox(height: 10),
          BigMenuButton(
            label: 'Perfil da aluna',
            subtitle: 'Interesses, dificuldades e estrategias que ajudam.',
            icon: Icons.person_outline,
            accentColor: AppTheme.softStar,
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ProfileScreen()),
            ),
          ),
          const SizedBox(height: 18),
          const _SectionTitle('Acompanhamento'),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _SmallAction(
                  label: 'Pais',
                  icon: Icons.family_restroom,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const ParentDashboardScreen()),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _SmallAction(
                  label: 'Microvitorias',
                  icon: Icons.stars,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const AchievementsScreen()),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          const _SafetyNote(),
        ],
      ),
    );
  }
}

class _HeroPanel extends StatelessWidget {
  const _HeroPanel({required this.onStart});

  final VoidCallback onStart;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppTheme.nightBlue,
        borderRadius: BorderRadius.circular(14),
      ),
      padding: const EdgeInsets.all(18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: AppTheme.softStar,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.auto_awesome, size: 28, color: AppTheme.nightBlue),
              ),
              const SizedBox(width: 12),
              const Expanded(
                child: Text(
                  'Apoio de estudo calmo, uma etapa por vez.',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 21,
                    fontWeight: FontWeight.w900,
                    height: 1.12,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          const Text(
            'Sem ranking, sem pressa. O app ajuda com pistas, rotina curta e acompanhamento dos responsaveis.',
            style: TextStyle(
              color: Color(0xFFE8EEF3),
              fontSize: 14,
              height: 1.35,
            ),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: onStart,
            icon: const Icon(Icons.school),
            label: const Text('Comecar estudo'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.softStar,
              foregroundColor: AppTheme.nightBlue,
            ),
          ),
          const SizedBox(height: 12),
          const _ApiBadge(),
        ],
      ),
    );
  }
}

class _ApiBadge extends StatelessWidget {
  const _ApiBadge();

  @override
  Widget build(BuildContext context) {
    const apiUrl = String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: 'http://10.0.2.2:8000',
    );

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.09),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
      ),
      child: Row(
        children: [
          const Icon(Icons.cloud_done_outlined, color: AppTheme.softStar, size: 18),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              'Backend: $apiUrl',
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700),
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(
        color: AppTheme.nightBlue,
        fontSize: 15,
        fontWeight: FontWeight.w900,
      ),
    );
  }
}

class _SmallAction extends StatelessWidget {
  const _SmallAction({
    required this.label,
    required this.icon,
    required this.onTap,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(10),
        onTap: onTap,
        child: SizedBox(
          height: 96,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: AppTheme.nightBlue, size: 26),
              const SizedBox(height: 8),
              Text(
                label,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: AppTheme.ink,
                  fontSize: 14,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SafetyNote extends StatelessWidget {
  const _SafetyNote();

  @override
  Widget build(BuildContext context) {
    return const Text(
      'Aviso: este app nao substitui escola, psicopedagoga, psicologa ou medico. Ele oferece apoio educacional.',
      textAlign: TextAlign.center,
      style: TextStyle(fontSize: 12, height: 1.35, color: AppTheme.muted),
    );
  }
}
