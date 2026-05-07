from app.schemas import ChatRequest

LOCK_PHRASES = [
    "não sei",
    "nao sei",
    "não consigo",
    "nao consigo",
    "sou burra",
    "sou incapaz",
    "travei",
    "estou travada",
    "ansiosa",
    "ansiedade",
]


def detect_support_mode(request: ChatRequest) -> bool:
    text = request.text.lower().strip()
    phrase_detected = any(phrase in text for phrase in LOCK_PHRASES)
    many_errors = request.recent_errors >= 2
    repeated_help = request.repeated_help_requests >= 2
    return phrase_detected or many_errors or repeated_help


def build_pedagogical_response(request: ChatRequest) -> dict:
    """Gera uma resposta local em JSON, pronta para substituição futura por IA real.

    A função não entrega a resposta completa de início. Ela acolhe, divide a tarefa
    e faz uma pergunta por vez, seguindo as regras pedagógicas do MVP.
    """
    support_mode = detect_support_mode(request)
    topic = request.subject if request.subject != "geral" else "essa atividade"

    if support_mode:
        answer = "Tudo bem travar. A gente vai diminuir o tamanho do passo agora."
        steps = [
            {"kind": "acolhimento", "text": "Você não precisa resolver tudo de uma vez."},
            {"kind": "redução", "text": "Vamos olhar só para a primeira informação importante."},
            {"kind": "exemplo", "text": "É como aprender uma coreografia: primeiro um movimento, depois outro."},
        ]
        question = "Qual opção você prefere agora: uma pista, um exemplo ou fazer junto?"
        options = ["Quero uma pista", "Quero um exemplo", "Quero fazer junto"]
        achievement = "Pediu apoio quando precisava"
    elif request.mode == "me_ajuda_com_a_tarefa":
        answer = "Vamos descobrir o que a questão pede, sem correr."
        steps = [
            {"kind": "acolhimento", "text": "Boa escolha pedir ajuda para começar."},
            {"kind": "divisão", "text": "Primeiro, vamos separar o enunciado em partes pequenas."},
            {"kind": "pista", "text": "Procure palavras como calcule, explique, compare ou marque."},
        ]
        question = "Qual é a primeira informação importante que aparece no enunciado?"
        options = ["Ler de novo", "Marcar palavras importantes", "Ver um exemplo parecido"]
        achievement = "Começou uma etapa"
    elif request.mode == "pausa_para_respirar":
        answer = "Vamos fazer uma pausa curta e segura."
        steps = [
            {"kind": "respiração", "text": "Inspire pelo nariz contando até 3."},
            {"kind": "respiração", "text": "Solte o ar devagar contando até 4."},
            {"kind": "retorno", "text": "Depois, vamos voltar só para o primeiro passo."},
        ]
        question = "Você quer voltar para a tarefa ou respirar mais uma vez?"
        options = ["Voltar para a tarefa", "Respirar mais uma vez", "Pedir ajuda a um responsável"]
        achievement = "Fez pausa e voltou"
    else:
        answer = f"Vamos estudar {topic} bem devagar, em partes pequenas."
        steps = [
            {"kind": "acolhimento", "text": "Você já deu o primeiro passo: começou."},
            {"kind": "explicação", "text": "Vou explicar com frases curtas e exemplo concreto."},
            {"kind": "analogia", "text": "Pense como numa música: primeiro ouvimos o ritmo, depois cantamos uma parte."},
        ]
        question = "Qual parte você quer entender primeiro?"
        options = ["Ver uma pista", "Ver um exemplo", "Fazer junto"]
        achievement = "Começou sozinha"

    raw = {
        "support_mode": support_mode,
        "emotional_tone": "acolhedor e calmo",
        "answer": answer,
        "steps": steps,
        "question_for_student": question,
        "hint_options": options,
        "achievement_suggestion": achievement,
        "safety_note": "Este app não substitui escola, psicopedagoga, psicóloga ou médico.",
    }
    return raw
