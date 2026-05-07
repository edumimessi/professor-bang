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
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(22),
              child: Column(
                children: [
                  Container(
                    width: 96,
                    height: 96,
                    decoration: const BoxDecoration(
                      color: AppTheme.softStar,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.auto_awesome, size: 48, color: AppTheme.nightBlue),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Oi. Eu vou estudar com você, sem pressa e uma parte por vez.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'Aqui não tem ranking. Tem calma, pistas e microvitórias.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 18),
          BigMenuButton(
            label: 'Começar estudo',
            icon: Icons.school,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const StudyModesScreen())),
          ),
          const SizedBox(height: 12),
          BigMenuButton(
            label: 'Chat pedagógico',
            icon: Icons.chat_bubble_outline,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ChatScreen(initialMode: 'Me explica devagar'))),
          ),
          const SizedBox(height: 12),
          BigMenuButton(
            label: 'Rotina de estudo',
            icon: Icons.checklist,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RoutineScreen())),
          ),
          const SizedBox(height: 12),
          BigMenuButton(
            label: 'Perfil da aluna',
            icon: Icons.person_outline,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ProfileScreen())),
          ),
          const SizedBox(height: 12),
          BigMenuButton(
            label: 'Painel dos pais',
            icon: Icons.family_restroom,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ParentDashboardScreen())),
          ),
          const SizedBox(height: 12),
          BigMenuButton(
            label: 'Microvitórias',
            icon: Icons.stars,
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AchievementsScreen())),
          ),
          const SizedBox(height: 20),
          const Text(
            'Aviso: este app não substitui escola, psicopedagoga, psicóloga ou médico. Ele não oferece orientação médica.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: Colors.black54),
          ),
        ],
      ),
    );
  }
}
