import 'package:flutter/foundation.dart';

import '../models/student_profile.dart';

class AppState extends ChangeNotifier {
  StudentProfile profile = StudentProfile.demo();

  void updateProfile(StudentProfile updatedProfile) {
    profile = updatedProfile;
    notifyListeners();
  }
}
