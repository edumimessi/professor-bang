class PedagogicalResponse {
  final bool supportMode;
  final String emotionalTone;
  final String answer;
  final List<String> steps;
  final String questionForStudent;
  final List<String> hintOptions;
  final String? achievementSuggestion;

  PedagogicalResponse({
    required this.supportMode,
    required this.emotionalTone,
    required this.answer,
    required this.steps,
    required this.questionForStudent,
    required this.hintOptions,
    this.achievementSuggestion,
  });

  String toReadableText() {
    final buffer = StringBuffer()
      ..writeln(answer)
      ..writeln();
    for (final step in steps) {
      buffer.writeln('• $step');
    }
    buffer
      ..writeln()
      ..writeln(questionForStudent);
    return buffer.toString().trim();
  }
}
