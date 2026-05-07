import 'package:flutter/material.dart';

import '../screens/home_screen.dart';
import 'app_theme.dart';

class ProfessorBangApp extends StatelessWidget {
  const ProfessorBangApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Professor Bang',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const HomeScreen(),
    );
  }
}
