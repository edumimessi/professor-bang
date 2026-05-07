import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/pedagogical_response.dart';
import '../models/student_profile.dart';

class ApiService {
  ApiService({
    String? baseUrl,
    http.Client? client,
  })  : baseUrl = (baseUrl ?? _defaultBaseUrl).replaceAll(RegExp(r'/+$'), ''),
        _client = client ?? http.Client();

  static const String _defaultBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  final String baseUrl;
  final http.Client _client;

  Uri _uri(String path) => Uri.parse('$baseUrl$path');

  Future<Map<String, dynamic>> _decodeJson(http.Response response) async {
    final body = utf8.decode(response.bodyBytes);
    final decoded = body.isEmpty ? <String, dynamic>{} : jsonDecode(body);
    if (decoded is Map<String, dynamic>) return decoded;
    throw Exception('Resposta inesperada da API.');
  }

  Future<http.Response> _request(Future<http.Response> Function() call) async {
    try {
      final response = await call().timeout(const Duration(seconds: 20));
      if (response.statusCode >= 400) {
        throw Exception(
          'API retornou erro ${response.statusCode}: ${utf8.decode(response.bodyBytes)}',
        );
      }
      return response;
    } on TimeoutException {
      throw Exception('Tempo esgotado ao conectar com $baseUrl.');
    } catch (error) {
      throw Exception('Falha ao conectar com $baseUrl. Detalhes: $error');
    }
  }

  Future<bool> healthCheck() async {
    final response = await _request(() => _client.get(_uri('/health')));
    final json = await _decodeJson(response);
    return json['status'] == 'ok';
  }

  Future<StudentProfile> createStudent(StudentProfile profile) async {
    final response = await _request(
      () => _client.post(
        _uri('/students/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(profile.toApiJson()),
      ),
    );
    return StudentProfile.fromJson(await _decodeJson(response));
  }

  Future<int> startSession({
    required int studentId,
    required String subject,
    required String studyMode,
  }) async {
    final response = await _request(
      () => _client.post(
        _uri('/sessions/start'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'student_id': studentId,
          'subject': subject,
          'study_mode': _mapMode(studyMode),
        }),
      ),
    );
    final json = await _decodeJson(response);
    return json['id'] as int;
  }

  Future<PedagogicalResponse> sendPedagogicalMessage({
    required int sessionId,
    required String text,
    required String mode,
    String subject = 'geral',
  }) async {
    final response = await _request(
      () => _client.post(
        _uri('/chat/message'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'session_id': sessionId,
          'message': text,
          'subject': subject,
          'study_mode': _mapMode(mode),
        }),
      ),
    );

    return PedagogicalResponse.fromBackendJson(await _decodeJson(response));
  }

  Future<List<Map<String, dynamic>>> getTodayRoutine(int studentId) async {
    final response = await _request(() => _client.get(_uri('/routine/$studentId/today')));
    final decoded = jsonDecode(utf8.decode(response.bodyBytes));
    return (decoded as List<dynamic>).cast<Map<String, dynamic>>();
  }

  Future<Map<String, dynamic>> getParentsReport(int studentId) async {
    final response = await _request(() => _client.get(_uri('/parents/$studentId/report')));
    return _decodeJson(response);
  }

  String _mapMode(String mode) {
    final normalized = mode.toLowerCase();
    if (normalized.contains('travada')) return 'apoio_travamento';
    if (normalized.contains('respirar') || normalized.contains('pausa')) return 'pausa_regulacao';
    if (normalized.contains('prova')) return 'treino_prova';
    if (normalized.contains('exemplo')) return 'exemplo_guiado';
    if (normalized.contains('tarefa')) return 'tarefa_guiada';
    if (normalized.contains('repetir')) return 'repeticao_calma';
    return 'explicacao_guiada';
  }
}
