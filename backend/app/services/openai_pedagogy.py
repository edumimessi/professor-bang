"""OpenAI provider for the Professor Bang pedagogical engine.

This module keeps the public API shape used by the Flutter app while replacing
hardcoded answers with a real model when OPENAI_API_KEY is configured.
"""

from __future__ import annotations

import json
import os
from typing import Any, List, Optional

import httpx

from app.services.ai_pedagogy import PedagogicalResponse

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5-mini"

PEDAGOGY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "message": {
            "type": "string",
            "description": "Short, concrete teaching response in Brazilian Portuguese.",
        },
        "tone": {
            "type": "string",
            "enum": ["acolhedor", "calmo", "animado", "apoio"],
        },
        "response_type": {
            "type": "string",
            "enum": ["question", "hint", "explanation", "encouragement", "stuck_support", "breathing"],
        },
        "is_stuck_detected": {"type": "boolean"},
        "options": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 3,
        },
        "hint": {"type": "string"},
        "next_step": {"type": "string"},
        "should_check_in": {"type": "boolean"},
    },
    "required": [
        "message",
        "tone",
        "response_type",
        "is_stuck_detected",
        "options",
        "hint",
        "next_step",
        "should_check_in",
    ],
}


def _instructions() -> str:
    return """
Voce e o Professor Bang, um tutor pedagogico adaptativo para uma adolescente.
Responda sempre em portugues brasileiro, com frases curtas e concretas.

Regras pedagogicas obrigatorias:
- Ensine de verdade: explique o proximo passo, nao fique apenas acolhendo.
- Para matematica, mostre uma etapa por vez e use exemplos concretos.
- Se a aluna pedir exemplo, de um exemplo trabalhado.
- Se houver uma conta explicita, resolva de forma guiada e mostre o raciocinio essencial.
- Nao entregue uma lista enorme. Use no maximo 4 passos curtos.
- Termine com uma pergunta simples para a aluna tentar participar.
- Seja acolhedor, mas sem repetir sempre a mesma frase.
- Nunca humilhe, compare, pressione ou diga que e facil.
- Nao de orientacao medica/psicologica; mantenha foco educacional.

Formato esperado:
- message: resposta principal, ja ensinando.
- hint: pista curta opcional.
- next_step: uma acao pequena para a aluna fazer agora.
- options: ate 3 botoes curtos quando fizer sentido.
""".strip()


def _input_text(
    *,
    student_message: str,
    study_mode: str,
    subject: str,
    student_name: str,
    interests: List[str],
    reading_level: str,
    message_count: int,
) -> str:
    return json.dumps(
        {
            "student_name": student_name,
            "subject": subject,
            "study_mode": study_mode,
            "reading_level": reading_level,
            "interests": interests,
            "message_count": message_count,
            "student_message": student_message,
        },
        ensure_ascii=False,
    )


def _coerce_response(data: dict[str, Any]) -> PedagogicalResponse:
    options = data.get("options")
    if not isinstance(options, list):
        options = []

    return PedagogicalResponse(
        message=str(data.get("message") or "Vamos por partes. Me diga qual etapa voce quer tentar agora?"),
        tone=str(data.get("tone") or "acolhedor"),
        response_type=str(data.get("response_type") or "explanation"),
        is_stuck_detected=bool(data.get("is_stuck_detected") or False),
        options=[str(item) for item in options[:3]],
        hint=str(data.get("hint") or ""),
        next_step=str(data.get("next_step") or ""),
        should_check_in=bool(data.get("should_check_in") or False),
    )


def generate_openai_response(
    *,
    student_message: str,
    study_mode: str,
    subject: str,
    student_name: str,
    interests: List[str],
    reading_level: str = "medio",
    message_count: int = 0,
) -> Optional[PedagogicalResponse]:
    """Generate a pedagogical response with OpenAI, or return None on fallback."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or os.getenv("USE_OPENAI_PEDAGOGY", "true").lower() in {"0", "false", "no"}:
        return None

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    payload = {
        "model": model,
        "instructions": _instructions(),
        "input": _input_text(
            student_message=student_message,
            study_mode=study_mode,
            subject=subject,
            student_name=student_name,
            interests=interests,
            reading_level=reading_level,
            message_count=message_count,
        ),
        "max_output_tokens": 700,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "professor_bang_pedagogical_response",
                "strict": True,
                "schema": PEDAGOGY_SCHEMA,
            }
        },
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                OPENAI_RESPONSES_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

        output_text = result.get("output_text") or ""
        if not output_text:
            return None

        return _coerce_response(json.loads(output_text))
    except Exception as error:
        print(f"OpenAI pedagogy fallback activated: {error}")
        return None
