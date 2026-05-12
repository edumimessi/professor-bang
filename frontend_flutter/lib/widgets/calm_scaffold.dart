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
        actions: actions,
      ),
      body: Container(
        color: AppTheme.cloudWhite,
        child: SafeArea(child: child),
      ),
    );
  }
}
