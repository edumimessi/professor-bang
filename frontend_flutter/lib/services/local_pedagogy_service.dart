import '../models/pedagogical_response.dart';

class LocalPedagogyService {
  static const List<String> _lockPhrases = [
    'não sei',
    'nao sei',
    'não consigo',
    'nao consigo',
    'travei',
    'travada',
    'ansiosa',
    'ansiedade',
    'sou burra',
    'incapaz',
  ];

  PedagogicalResponse respond({
    required String text,
    required String mode,
    int repeatedHelpRequests = 0,
    int recentErrors = 0,
  }) {
    final normalized = text.toLowerCase();
    final supportMode = _lockPhrases.any(normalized.contains) ||
        repeatedHelpRequests >= 2 ||
        recentErrors >= 2 ||
        mode == 'Estou travada';

    if (supportMode) {
      return PedagogicalResponse(
        supportMode: true,
        emotionalTone: 'acolhedor e calmo',
        answer: 'Tudo bem travar. Vamos diminuir o passo agora.',
        steps: const [
          'Você não precisa resolver tudo de uma vez.',
          'Vamos olhar só para a primeira informação importante.',
          'É como aprender uma coreografia: primeiro um movimento, depois outro.',
        ],
        questionForStudent: 'O que você prefere agora?',
        hintOptions: const ['Quero uma pista', 'Quero um exemplo', 'Quero fazer junto'],
        achievementSuggestion: 'Pediu apoio quando precisava',
      );
    }

    if (mode == 'Me ajuda com a tarefa') {
      return PedagogicalResponse(
        supportMode: false,
        emotionalTone: 'orientador',
        answer: 'Vamos descobrir o que a questão pede, sem correr.',
        steps: const [
          'Primeiro, leia só a primeira frase.',
          'Depois, procure palavras como calcule, explique, compare ou marque.',
          'Não vamos fazer tudo agora. Só vamos encontrar o primeiro passo.',
        ],
        questionForStudent: 'Qual é a primeira informação importante do enunciado?',
        hintOptions: const ['Ler de novo', 'Marcar palavras importantes', 'Ver exemplo parecido'],
        achievementSuggestion: 'Começou uma etapa',
      );
    }

    if (mode == 'Pausa para respirar') {
      return PedagogicalResponse(
        supportMode: false,
        emotionalTone: 'regulação emocional',
        answer: 'Vamos fazer uma pausa curta e segura.',
        steps: const [
          'Inspire pelo nariz contando até 3.',
          'Solte o ar devagar contando até 4.',
          'Quando estiver pronta, voltamos só para um passo.',
        ],
        questionForStudent: 'Você quer voltar para a tarefa ou respirar mais uma vez?',
        hintOptions: const ['Voltar para a tarefa', 'Respirar mais uma vez', 'Pedir ajuda a um responsável'],
        achievementSuggestion: 'Fez pausa e voltou',
      );
    }

    return PedagogicalResponse(
      supportMode: false,
      emotionalTone: 'motivador',
      answer: 'Vamos estudar bem devagar, em partes pequenas.',
      steps: const [
        'Você já deu o primeiro passo: começou.',
        'Vou usar frases curtas e exemplo concreto.',
        'Pense como numa música: primeiro o ritmo, depois uma parte da letra.',
      ],
      questionForStudent: 'Qual parte você quer entender primeiro?',
      hintOptions: const ['Ver uma pista', 'Ver um exemplo', 'Fazer junto'],
      achievementSuggestion: 'Começou sozinha',
    );
  }
}
