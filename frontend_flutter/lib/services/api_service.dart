import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/pedagogical_response.dart';

class ApiService {
  ApiService({this.baseUrl = 'http://localhost:8000/api'});

  final String baseUrl;

  Future<PedagogicalResponse> sendPedagogicalMessage({
    required String text,
    required String mode,
    String subject = 'geral',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/pedagogical'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'text': text, 'mode': mode, 'subject': subject}),
    );

    if (response.statusCode >= 400) {
      throw Exception('Falha ao falar com a API pedagógica.');
    }

    final json = jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    final steps = (json['steps'] as List<dynamic>)
        .map((item) => item is Map<String, dynamic> ? item['text'].toString() : item.toString())
        .toList();

    return PedagogicalResponse(
      supportMode: json['support_mode'] as bool? ?? false,
      emotionalTone: json['emotional_tone']?.toString() ?? 'acolhedor',
      answer: json['answer']?.toString() ?? '',
      steps: steps,
      questionForStudent: json['question_for_student']?.toString() ?? '',
      hintOptions: (json['hint_options'] as List<dynamic>? ?? const []).map((e) => e.toString()).toList(),
      achievementSuggestion: json['achievement_suggestion']?.toString(),
    );
  }
}
