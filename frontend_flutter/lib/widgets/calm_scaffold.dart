import 'package:flutter/material.dart';

import '../app/app_theme.dart';

class CalmScaffold extends StatelessWidget {
  const CalmScaffold({
    super.key,
    required this.title,
    required this.child,
    this.actions,
  });

  final String title;
  final Widget child;
  final List<Widget>? actions;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        backgroundColor: AppTheme.nightBlue,
        foregroundColor: Colors.white,
        actions: actions,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppTheme.nightBlue, AppTheme.cloudWhite],
            stops: [0.0, 0.38],
          ),
        ),
        child: SafeArea(child: child),
      ),
    );
  }
}
