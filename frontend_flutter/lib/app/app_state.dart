import 'package:flutter/foundation.dart';

import '../models/student_profile.dart';
import '../services/api_service.dart';

class AppState extends ChangeNotifier {
  AppState({ApiService? api}) : api = api ?? ApiService();

  final ApiService api;

  StudentProfile profile = StudentProfile.demo();
  int? remoteStudentId;
  int? activeSessionId;
  String? lastConnectionError;

  bool get hasRemoteProfile => remoteStudentId != null;

  void updateProfile(StudentProfile updatedProfile) {
    profile = updatedProfile;
    remoteStudentId = updatedProfile.id ?? remoteStudentId;
    notifyListeners();
  }

  Future<StudentProfile> saveProfileToApi() async {
    try {
      final saved = await api.createStudent(profile);
      profile = saved;
      remoteStudentId = saved.id;
      lastConnectionError = null;
      notifyListeners();
      return saved;
    } catch (error) {
      lastConnectionError = error.toString();
      notifyListeners();
      rethrow;
    }
  }

  Future<int> ensureRemoteProfile() async {
    if (remoteStudentId != null) return remoteStudentId!;
    final saved = await saveProfileToApi();
    return saved.id!;
  }

  Future<int> startStudySession({
    required String subject,
    required String studyMode,
  }) async {
    final studentId = await ensureRemoteProfile();
    final sessionId = await api.startSession(
      studentId: studentId,
      subject: subject,
      studyMode: studyMode,
    );
    activeSessionId = sessionId;
    lastConnectionError = null;
    notifyListeners();
    return sessionId;
  }
}
