class StudentProfile {
  final String name;
  final int age;
  final String difficultSubjects;
  final String interests;
  final String readingLevel;
  final String mathLevel;
  final String anxietyTriggers;
  final String helpfulStrategies;

  const StudentProfile({
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
      readingLevel: 'frases curtas e concretas',
      mathLevel: 'operações passo a passo',
      anxietyTriggers: 'pressa, texto longo e muitas etapas juntas',
      helpfulStrategies: 'pistas, exemplos simples e pausa para respirar',
    );
  }

  Map<String, dynamic> toMap() => {
        'name': name,
        'age': age,
        'difficultSubjects': difficultSubjects,
        'interests': interests,
        'readingLevel': readingLevel,
        'mathLevel': mathLevel,
        'anxietyTriggers': anxietyTriggers,
        'helpfulStrategies': helpfulStrategies,
      };
}
