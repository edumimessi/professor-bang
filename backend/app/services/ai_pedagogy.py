# backend/app/services/ai_pedagogy.py
#
# Motor de IA Pedagógica — versão MVP com regras hardcoded.
# Substituível por chamada OpenAI GPT-4 quando disponível.
#
# PRINCÍPIOS:
#   1. Nunca dar a resposta completa de uma vez.
#   2. Sempre terminar com uma pergunta.
#   3. Detectar travamento e acionar Modo Apoio.
#   4. Usar analogias com os interesses da aluna.
#   5. Reforçar o esforço, nunca o resultado.

from dataclasses import dataclass
from typing import Optional, List
import re
import random


# ─────────────────────────────────────────────────────────────
# Tipos de resposta pedagógica
# ─────────────────────────────────────────────────────────────

RESPONSE_TYPES = {
    "welcome":       "Boas-vindas à sessão",
    "question":      "Pergunta socrática",
    "hint":          "Pista leve",
    "explanation":   "Explicação passo a passo",
    "encouragement": "Reforço de esforço",
    "stuck_support": "Modo Apoio (travamento detectado)",
    "breathing":     "Exercício de respiração",
    "summary":       "Resumo do que aprendeu",
}


@dataclass
class PedagogicalResponse:
    message: str
    tone: str                         # acolhedor | animado | calmo | apoio
    response_type: str
    is_stuck_detected: bool = False
    options: Optional[List[str]] = None  # opções clicáveis no Modo Apoio
    hint: Optional[str] = None
    next_step: Optional[str] = None
    should_check_in: bool = False


# ─────────────────────────────────────────────────────────────
# Palavras-chave de travamento
# ─────────────────────────────────────────────────────────────

STUCK_KEYWORDS = [
    "não sei", "nao sei", "não entendo", "nao entendo",
    "não entendi", "nao entendi", "não tô entendendo", "nao to entendendo",
    "não consigo", "nao consigo", "tá difícil", "ta difícil",
    "tô perdida", "to perdida", "travada", "travado", "desisti", "odeio",
    "não aguento", "nao aguento", "burra", "idiota",
    "impossível", "impossivel", "não vou conseguir",
    "esqueci tudo", "não lembro", "nao lembro",
    "ajuda", "socorro", "não faço ideia",
]

FRUSTRATION_KEYWORDS = [
    "odeio", "detesto", "chato", "horrível", "ruim",
    "cansada", "tô mal", "to mal", "ansiosa", "nervosa",
    "medo", "assustada",
]


# ─────────────────────────────────────────────────────────────
# Analogias por interesse
# ─────────────────────────────────────────────────────────────

ANALOGIES: dict[str, dict] = {
    "K-pop": {
        "Matemática": "Pensa assim: uma sequência matemática é como a coreografia de um grupo de K-pop — cada movimento (número) segue uma regra e vem depois do anterior! 🎵",
        "Português": "Estruturar um texto é como montar um álbum de K-pop: tem intro, as músicas principais e o encerramento. Cada parte tem um papel!",
        "default": "É como aprender uma coreografia nova: parece difícil no começo, mas a gente vai passo a passo! 🎶",
    },
    "Dança": {
        "Matemática": "Cada operação matemática é um passo de dança: você aprende um de cada vez, depois vai encadeando!",
        "Português": "Escrever bem é como improvisar na dança — você conhece os movimentos básicos e aí cria o seu estilo!",
        "default": "Vai devagar, como quando você aprende um passo novo: repetição com calma faz a diferença! 💃",
    },
    "Games": {
        "Matemática": "Pensa que resolver uma equação é tipo um puzzle de game: você tem as peças (números) e precisa descobrir onde cada uma encaixa!",
        "Português": "Escrever um texto é como criar um personagem: você define as características (argumentos) e constrói a história!",
        "default": "Cada conceito novo é um level up — difícil no começo, mas você passa! 🎮",
    },
    "Música": {
        "Matemática": "Frações são como compassos musicais: 1/4 é uma semínima, 1/2 é uma mínima... tudo se divide!",
        "Português": "A pontuação no texto é como as pausas numa música: ela dá ritmo e sentido!",
        "default": "Aprender é como tocar uma música nova: primeiro você vai devagar, depois o ritmo vem! 🎸",
    },
    "Animes": {
        "Matemática": "O Naruto não virou Hokage de um dia pro outro — cada treino é uma equação resolvida!",
        "Português": "Escrever bem é como desenvolver um personagem de anime: quanto mais profundidade, mais interessante fica!",
        "default": "Todo protagonista começa do zero. A diferença é que eles não desistem! ✨",
    },
    "default": {
        "default": "Vamos quebrar isso em partes menores — fica mais fácil assim!",
    },
}


def _get_analogy(interests: List[str], subject: str) -> str:
    """Retorna analogia personalizada pelo interesse e matéria."""
    for interest in interests:
        interest_map = ANALOGIES.get(interest)
        if interest_map:
            return interest_map.get(subject, interest_map.get("default", ""))
    return ANALOGIES["default"]["default"]


# ─────────────────────────────────────────────────────────────
# Motor principal
# ─────────────────────────────────────────────────────────────

class PedagogyEngine:
    """
    Motor de IA pedagógica local.
    Recebe contexto da sessão e gera resposta adaptada.
    """

    def __init__(self):
        self._error_streak: dict[int, int] = {}   # session_id → contagem de erros

    # ── Ponto de entrada ──────────────────────────────────────

    def generate_response(
        self,
        session_id: int,
        student_message: str,
        study_mode: str,
        subject: str,
        student_name: str,
        interests: List[str],
        reading_level: str = "medio",
        message_count: int = 0,
    ) -> PedagogicalResponse:
        """Gera resposta pedagógica baseada no modo de estudo e na mensagem."""

        msg = student_message.strip().lower()

        # Detecta travamento
        is_stuck = self._detect_stuck(msg)
        is_frustrated = self._detect_frustration(msg)

        # Atualiza streak de erros
        if is_stuck:
            self._error_streak[session_id] = self._error_streak.get(session_id, 0) + 1
        else:
            self._error_streak[session_id] = 0

        stuck_count = self._error_streak.get(session_id, 0)

        # Modo Apoio ativado quando há travamento explícito ou repetido.
        # Em contexto de dificuldade cognitiva/ansiedade escolar, a primeira
        # frase de bloqueio já deve receber apoio acolhedor e estruturado.
        if is_stuck or stuck_count >= 2 or "ajuda" in msg or "modo apoio" in msg:
            return self._stuck_response(student_name, subject, interests)

        # Exercício de respiração
        if study_mode == "breathing" or is_frustrated:
            return self._breathing_response(student_name)

        # Roteamento por modo
        handlers = {
            "explain_slow": self._explain_slow,
            "help_homework": self._help_homework,
            "give_example":  self._give_example,
            "repeat":        self._repeat_response,
            "stuck":         lambda n, s, i, m: self._stuck_response(n, s, i),
            "practice_test": self._practice_test,
        }

        handler = handlers.get(study_mode, self._default_response)

        if study_mode in ("stuck",):
            return handler(student_name, subject, interests, msg)
        return handler(student_name, subject, interests, msg)

    def generate_welcome(
        self,
        student_name: str,
        subject: str,
        study_mode: str,
        interests: List[str],
    ) -> PedagogicalResponse:
        """Mensagem de boas-vindas ao iniciar sessão."""
        mode_labels = {
            "explain_slow":  "devagar e com calma",
            "help_homework": "com a lição de casa",
            "give_example":  "com um exemplo",
            "repeat":        "repetindo de outro jeito",
            "stuck":         "com apoio total",
            "practice_test": "praticando",
            "breathing":     "com respiração",
        }
        mode_label = mode_labels.get(study_mode, "estudando")
        analogy = _get_analogy(interests, subject)

        msg = (
            f"Oi, {student_name}! 🌟 Que bom ter você aqui.\n\n"
            f"Hoje a gente vai trabalhar **{subject}** — {mode_label}.\n\n"
            f"{analogy}\n\n"
            f"Me conta: o que você quer entender hoje?"
        )
        return PedagogicalResponse(
            message=msg,
            tone="acolhedor",
            response_type="welcome",
        )

    # ── Handlers por modo ────────────────────────────────────

    def _explain_slow(self, name, subject, interests, msg) -> PedagogicalResponse:
        analogy = _get_analogy(interests, subject)
        responses = [
            f"Ótimo! Antes de a gente começar, me conta: o que você já sabe sobre isso?",
            f"Certo! Vamos com calma. {analogy}\n\nQual parte ficou mais confusa pra você?",
            f"Entendido! Vou explicar em partes pequenas, tá? Qual foi a última coisa que fez sentido pra você?",
        ]
        return PedagogicalResponse(
            message=random.choice(responses),
            tone="calmo",
            response_type="question",
        )

    def _help_homework(self, name, subject, interests, msg) -> PedagogicalResponse:
        responses = [
            "Vamos juntas! Primeiro: me copia aqui o enunciado do exercício. O que está pedindo?",
            f"Que exercício é esse? Me conta o que está escrito — a gente identifica o que é pedido primeiro.",
            "Antes de resolver, a gente precisa entender o que a questão quer. O que você leu até agora?",
        ]
        return PedagogicalResponse(
            message=random.choice(responses),
            tone="acolhedor",
            response_type="question",
            hint="Leia o enunciado em voz alta — isso ajuda muito a entender o que está sendo pedido!",
        )

    def _give_example(self, name, subject, interests, msg) -> PedagogicalResponse:
        analogy = _get_analogy(interests, subject)
        msg_out = (
            f"{analogy}\n\n"
            f"Depois desse exemplo, o que fez mais sentido pra você?"
        )
        return PedagogicalResponse(
            message=msg_out,
            tone="animado",
            response_type="explanation",
        )

    def _repeat_response(self, name, subject, interests, msg) -> PedagogicalResponse:
        responses = [
            "Sem problema — cada pessoa entende de um jeito diferente, e isso é normal! 💙\n\nVou explicar de outro ângulo: qual parte ficou mais nebulosa?",
            "Claro! Vamos tentar de outro jeito. O que você entendeu até agora, mesmo que seja pouquinho?",
            "Tranquilo! Às vezes basta uma palavra diferente pra fazer clique. Me fala: o que você acha que está te confundindo?",
        ]
        return PedagogicalResponse(
            message=random.choice(responses),
            tone="calmo",
            response_type="explanation",
        )

    def _practice_test(self, name, subject, interests, msg) -> PedagogicalResponse:
        return PedagogicalResponse(
            message=(
                f"Ótimo, vamos praticar! 💪\n\n"
                f"Aqui vai uma questão de cada vez, sem pressa.\n\n"
                f"Me conta: você quer começar por algo que está mais segura, ou pelo que está mais difícil?"
            ),
            tone="animado",
            response_type="question",
        )

    def _default_response(self, name, subject, interests, msg) -> PedagogicalResponse:
        return PedagogicalResponse(
            message=f"Entendido! Me conta mais — o que exatamente está travando?",
            tone="acolhedor",
            response_type="question",
        )

    # ── Respostas especiais ───────────────────────────────────

    def _stuck_response(self, name: str, subject: str, interests: List[str]) -> PedagogicalResponse:
        """Modo Apoio: oferece 3 opções clicáveis."""
        analogy = _get_analogy(interests, subject)
        return PedagogicalResponse(
            message=(
                f"Tá tudo bem, {name}. 💙 Travar faz parte do processo — até quem entende muito já ficou assim.\n\n"
                f"A gente vai sair disso juntas. Como você quer que eu te ajude agora?"
            ),
            tone="apoio",
            response_type="stuck_support",
            is_stuck_detected=True,
            options=[
                "💡 Me dá uma pista",
                "🔍 Me mostra um exemplo",
                "🤝 Faz comigo, passo a passo",
            ],
            hint=analogy,
            should_check_in=True,
        )

    def _breathing_response(self, name: str) -> PedagogicalResponse:
        return PedagogicalResponse(
            message=(
                f"Vamos pausar um segundo, {name}. 🌸\n\n"
                f"**Respiração 4-2-6:**\n"
                f"• Inspira pelo nariz contando até **4**\n"
                f"• Segura contando até **2**\n"
                f"• Solta devagar pela boca contando até **6**\n\n"
                f"Repita 3 vezes. Quando quiser continuar, é só me avisar. 💙"
            ),
            tone="calmo",
            response_type="breathing",
        )

    def generate_success(self, name: str, subject: str) -> PedagogicalResponse:
        """Resposta de reforço ao acertar — reforça o esforço, não o resultado."""
        responses = [
            f"Isso! Você chegou lá, {name}! 🎉 Não foi porque é fácil — foi porque você persistiu.",
            f"Muito bem! 🌟 O que te fez chegar nessa resposta? Quero que você veja como você mesmo raciocinou.",
            f"Conseguiu! 💙 E olha: a próxima vez que aparecer algo parecido, você já vai saber por onde começar.",
        ]
        return PedagogicalResponse(
            message=random.choice(responses),
            tone="animado",
            response_type="encouragement",
        )

    # ── Detecção ─────────────────────────────────────────────

    def _detect_stuck(self, msg: str) -> bool:
        return any(kw in msg for kw in STUCK_KEYWORDS)

    def _detect_frustration(self, msg: str) -> bool:
        return any(kw in msg for kw in FRUSTRATION_KEYWORDS)

    def generate_pedagogical_note(
        self,
        week_sessions: int,
        stuck_moments: int,
        subjects: List[str],
    ) -> str:
        """Gera nota pedagógica para o relatório dos pais."""
        if week_sessions == 0:
            return "Nenhuma sessão registrada nesta semana."

        avg_stuck = stuck_moments / max(week_sessions, 1)
        subjects_str = ", ".join(subjects) if subjects else "variadas"

        if avg_stuck < 1:
            progress = "demonstrou boa fluidez nos estudos"
        elif avg_stuck < 3:
            progress = "está construindo confiança gradualmente"
        else:
            progress = "encontrou alguns pontos de dificuldade — o que é normal e esperado"

        return (
            f"Esta semana, a aluna realizou {week_sessions} sessão(ões) de estudo, "
            f"trabalhando as matérias: {subjects_str}. "
            f"Ela {progress}. "
            f"O app utilizou estratégias de reforço positivo e suporte gradual em todos os momentos de travamento. "
            f"Recomenda-se manter a rotina de estudo diária e celebrar cada pequeno avanço em casa."
        )


# Instância singleton
pedagogy_engine = PedagogyEngine()
