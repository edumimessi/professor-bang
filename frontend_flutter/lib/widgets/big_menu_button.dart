import 'package:flutter/material.dart';

class BigMenuButton extends StatelessWidget {
  const BigMenuButton({
    super.key,
    required this.label,
    required this.icon,
    required this.onTap,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: onTap,
      icon: Icon(icon, size: 26),
      label: Text(label),
    );
  }
}
