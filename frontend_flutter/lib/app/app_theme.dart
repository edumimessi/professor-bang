import 'package:flutter/material.dart';

class AppTheme {
  static const Color nightBlue = Color(0xFF17283A);
  static const Color calmBlue = Color(0xFF3A6C7E);
  static const Color moss = Color(0xFF6C7A45);
  static const Color softStar = Color(0xFFF4DFA1);
  static const Color cloudWhite = Color(0xFFF8F5EF);
  static const Color ink = Color(0xFF20272E);
  static const Color muted = Color(0xFF66717A);

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
      appBarTheme: const AppBarTheme(
        centerTitle: false,
        elevation: 0,
        backgroundColor: cloudWhite,
        foregroundColor: nightBlue,
        titleTextStyle: TextStyle(
          color: nightBlue,
          fontSize: 20,
          fontWeight: FontWeight.w800,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: nightBlue,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(54),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      ),
      cardTheme: CardThemeData(
        color: Colors.white,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
          side: const BorderSide(color: Color(0xFFE2DBCF)),
        ),
      ),
    );
  }
}
