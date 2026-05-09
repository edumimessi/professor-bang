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

  factory PedagogicalResponse.fromBackendJson(Map<String, dynamic> json) {
    final options = (json['options'] as List<dynamic>? ?? const [])
        .map((item) => item.toString())
        .toList();
    final hint = json['hint']?.toString();
    final nextStep = json['next_step']?.toString();
    final responseType = json['response_type']?.toString();

    return PedagogicalResponse(
      supportMode: json['is_stuck_detected'] as bool? ?? false,
      emotionalTone: json['tone']?.toString() ?? 'acolhedor',
      answer: json['message']?.toString() ?? '',
      steps: [
        if (hint != null && hint.trim().isNotEmpty) 'Pista: $hint',
        if (nextStep != null && nextStep.trim().isNotEmpty) 'Proximo passo: $nextStep',
      ],
      questionForStudent: options.isNotEmpty
          ? 'Escolha uma opcao para continuar: ${options.join(' | ')}'
          : 'Quer tentar responder com suas palavras?',
      hintOptions: options,
      achievementSuggestion: responseType == 'stuck_support'
          ? 'Pediu ajuda antes de desistir'
          : null,
    );
  }

  factory PedagogicalResponse.fromLegacyJson(Map<String, dynamic> json) {
    final steps = (json['steps'] as List<dynamic>? ?? const [])
        .map((item) => item is Map<String, dynamic> ? item['text'].toString() : item.toString())
        .toList();

    return PedagogicalResponse(
      supportMode: json['support_mode'] as bool? ?? false,
      emotionalTone: json['emotional_tone']?.toString() ?? 'acolhedor',
      answer: json['answer']?.toString() ?? '',
      steps: steps,
      questionForStudent: json['question_for_student']?.toString() ?? '',
      hintOptions: (json['hint_options'] as List<dynamic>? ?? const [])
          .map((item) => item.toString())
          .toList(),
      achievementSuggestion: json['achievement_suggestion']?.toString(),
    );
  }

  String toReadableText() {
    final buffer = StringBuffer();
    if (answer.trim().isNotEmpty) {
      buffer.writeln(answer.trim());
    }
    if (steps.isNotEmpty) {
      if (buffer.isNotEmpty) buffer.writeln();
      for (final step in steps) {
        buffer.writeln('- $step');
      }
    }
    if (questionForStudent.trim().isNotEmpty) {
      if (buffer.isNotEmpty) buffer.writeln();
      buffer.writeln(questionForStudent.trim());
    }
    return buffer.toString().trim();
  }
}
