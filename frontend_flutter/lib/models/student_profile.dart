class StudentProfile {
  final int? id;
  final String name;
  final int age;
  final String difficultSubjects;
  final String interests;
  final String readingLevel;
  final String mathLevel;
  final String anxietyTriggers;
  final String helpfulStrategies;

  const StudentProfile({
    this.id,
    required this.name,
    required this.age,
    required this.difficultSubjects,
    required this.interests,
    required this.readingLevel,
    required this.mathLevel,
    required this.anxietyTriggers,
    required this.helpfulStrategies,
  });

  factory StudentProfile.demo() {
    return const StudentProfile(
      name: 'Duda',
      age: 14,
      difficultSubjects: 'Matemática e interpretação de texto',
      interests: 'K-pop, dança, música e idiomas',
      readingLevel: 'medio',
      mathLevel: 'basico',
      anxietyTriggers: 'pressa, texto longo e muitas etapas juntas',
      helpfulStrategies: 'pistas, exemplos simples e pausa para respirar',
    );
  }

  factory StudentProfile.fromJson(Map<String, dynamic> json) {
    return StudentProfile(
      id: json['id'] as int?,
      name: json['name']?.toString() ?? 'Duda',
      age: json['age'] as int? ?? 14,
      difficultSubjects: _joinList(json['difficult_subjects']),
      interests: _joinList(json['interests']),
      readingLevel: json['reading_level']?.toString() ?? 'medio',
      mathLevel: json['math_level']?.toString() ?? 'basico',
      anxietyTriggers: _joinList(json['anxiety_triggers']),
      helpfulStrategies: _joinList(json['helpful_strategies']),
    );
  }

  Map<String, dynamic> toApiJson() => {
        'name': name,
        'age': age,
        'difficult_subjects': _splitList(difficultSubjects),
        'interests': _splitList(interests),
        'reading_level': readingLevel,
        'math_level': mathLevel,
        'anxiety_triggers': _splitList(anxietyTriggers),
        'helpful_strategies': _splitList(helpfulStrategies),
      };

  Map<String, dynamic> toMap() => {
        'id': id,
        'name': name,
        'age': age,
        'difficultSubjects': difficultSubjects,
        'interests': interests,
        'readingLevel': readingLevel,
        'mathLevel': mathLevel,
        'anxietyTriggers': anxietyTriggers,
        'helpfulStrategies': helpfulStrategies,
      };

  static List<String> _splitList(String value) {
    return value
        .split(RegExp(r'[,;\n]'))
        .map((item) => item.trim())
        .where((item) => item.isNotEmpty)
        .toList();
  }

  static String _joinList(dynamic value) {
    if (value is List) {
      return value.map((item) => item.toString()).join(', ');
    }
    return value?.toString() ?? '';
  }
}
