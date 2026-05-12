"""Gemini provider for the Professor Bang pedagogical engine."""

from __future__ import annotations

import json
import os
from typing import Any, List, Optional

import httpx

from app.services.ai_pedagogy import PedagogicalResponse

DEFAULT_MODEL = "gemini-2.5-flash"
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _instructions() -> str:
    return """
Voce e o Professor Bang, um tutor pedagogico adaptativo para uma adolescente.
Responda sempre em portugues brasileiro, com frases curtas e concretas.

Regras pedagogicas obrigatorias:
- Ensine de verdade: explique o proximo passo, nao fique apenas acolhendo.
- Use o historico recente para entender pedidos como "um exemplo" ou "faz comigo".
- Para matematica, mostre uma etapa por vez e use exemplos concretos.
- Se houver uma conta explicita, resolva de forma guiada e mostre o raciocinio essencial.
- Se a aluna pedir exemplo, de um exemplo trabalhado relacionado ao assunto atual.
- Nao entregue uma lista enorme. Use no maximo 4 passos curtos.
- Termine com uma pergunta simples para a aluna tentar participar.
- Seja acolhedor, mas sem repetir sempre a mesma frase.
- Nunca humilhe, compare, pressione ou diga que e facil.
- Nao de orientacao medica/psicologica; mantenha foco educacional.

Responda somente com um JSON valido neste formato:
{
  "message": "resposta principal, ja ensinando",
  "tone": "acolhedor",
  "response_type": "explanation",
  "is_stuck_detected": true,
  "options": ["Quero tentar", "Me da uma pista", "Outro exemplo"],
  "hint": "pista curta opcional",
  "next_step": "uma acao pequena para a aluna fazer agora",
  "should_check_in": false
}

Valores aceitos:
- tone: acolhedor, calmo, animado, apoio.
- response_type: question, hint, explanation, encouragement, stuck_support, breathing.
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
    recent_messages: List[dict[str, str]],
) -> str:
    return json.dumps(
        {
            "student_name": student_name,
            "subject": subject,
            "study_mode": study_mode,
            "reading_level": reading_level,
            "interests": interests,
            "message_count": message_count,
            "recent_messages": recent_messages[-8:],
            "student_message": student_message,
        },
        ensure_ascii=False,
    )


def _extract_output_text(result: dict[str, Any]) -> str:
    candidates = result.get("candidates") or []
    if not candidates:
        return ""

    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    chunks: list[str] = []
    for part in parts:
        text = part.get("text")
        if isinstance(text, str):
            chunks.append(text)
    return "".join(chunks).strip()


def _parse_json_text(text: str) -> dict[str, Any]:
    clean = text.strip()
    if clean.startswith("```"):
        clean = clean.strip("`").strip()
        if clean.lower().startswith("json"):
            clean = clean[4:].strip()
    return json.loads(clean)


def _coerce_response(data: dict[str, Any]) -> PedagogicalResponse:
    options = data.get("options")
    if not isinstance(options, list):
        options = []

    tone = str(data.get("tone") or "acolhedor")
    if tone not in {"acolhedor", "calmo", "animado", "apoio"}:
        tone = "acolhedor"

    response_type = str(data.get("response_type") or "explanation")
    if response_type not in {"question", "hint", "explanation", "encouragement", "stuck_support", "breathing"}:
        response_type = "explanation"

    return PedagogicalResponse(
        message=str(data.get("message") or "Vamos por partes. Me diga qual etapa voce quer tentar agora?"),
        tone=tone,
        response_type=response_type,
        is_stuck_detected=bool(data.get("is_stuck_detected") or False),
        options=[str(item) for item in options[:3]],
        hint=str(data.get("hint") or ""),
        next_step=str(data.get("next_step") or ""),
        should_check_in=bool(data.get("should_check_in") or False),
    )


def generate_gemini_response(
    *,
    student_message: str,
    study_mode: str,
    subject: str,
    student_name: str,
    interests: List[str],
    reading_level: str = "medio",
    message_count: int = 0,
    recent_messages: Optional[List[dict[str, str]]] = None,
) -> Optional[PedagogicalResponse]:
    """Generate a pedagogical response with Gemini, or return None on fallback."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or os.getenv("USE_GEMINI_PEDAGOGY", "true").lower() in {"0", "false", "no"}:
        return None

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    url = f"{GEMINI_API_BASE_URL}/{model}:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": _instructions()}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": _input_text(
                            student_message=student_message,
                            study_mode=study_mode,
                            subject=subject,
                            student_name=student_name,
                            interests=interests,
                            reading_level=reading_level,
                            message_count=message_count,
                            recent_messages=recent_messages or [],
                        )
                    }
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": 700,
            "responseMimeType": "application/json",
        },
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key,
                },
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

        output_text = _extract_output_text(result)
        if not output_text:
            return None

        return _coerce_response(_parse_json_text(output_text))
    except Exception as error:
        print(f"Gemini pedagogy fallback activated: {error}")
        return None
