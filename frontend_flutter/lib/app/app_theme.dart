import 'package:flutter/material.dart';

class AppTheme {
  static const Color nightBlue = Color(0xFF0B1B3F);
  static const Color calmBlue = Color(0xFF1E5AA8);
  static const Color softStar = Color(0xFFFFF4C2);
  static const Color cloudWhite = Color(0xFFF8FBFF);

  static ThemeData get lightTheme {
    return ThemeData(
      colorScheme: ColorScheme.fromSeed(
        seedColor: calmBlue,
        primary: nightBlue,
        secondary: calmBlue,
        surface: cloudWhite,
      ),
      scaffoldBackgroundColor: cloudWhite,
      useMaterial3: true,
      fontFamily: 'Roboto',
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: calmBlue,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(56),
          textStyle: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
        ),
      ),
      cardTheme: CardTheme(
        color: Colors.white,
        elevation: 1,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
      ),
    );
  }
}
