"""MCP-Server: Brücke zwischen LM Studio (localhost) und Cursor.

Stellt LM-Studio-Chat und einen zweistufigen Review-Workflow bereit:
  1. Erstinstanz (`review_analyze`) — kritische Erstbewertung
  2. Zweitinstanz (`review_confirm`) — unabhängige Bestätigung der Erstbewertung

Cursor-Konfiguration (Beispiel siehe tools/model_server.mcp.json.example):

    python tools/model_server.py

Umgebungsvariablen:
    LMSTUDIO_BASE_URL          — Default: http://localhost:1234
    LMSTUDIO_MODEL             — Chat-Modell-ID (sonst Auto-Auswahl)
    LMSTUDIO_REVIEW_MODEL      — Optional separates Review-Modell
    LMSTUDIO_CONFIRM_MODEL     — Optional separates Bestätigungs-Modell
    LMSTUDIO_TIMEOUT_S         — HTTP-Timeout (Default: 120)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_BASE_URL = "http://localhost:1234"
DEFAULT_TIMEOUT_S = 120.0
EMBED_HINTS = ("embed", "embedding", "nomic-embed")

logger = logging.getLogger("model_server")


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr,
    )


def _base_url() -> str:
    return os.environ.get("LMSTUDIO_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _timeout_s() -> float:
    return float(os.environ.get("LMSTUDIO_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))


def _http_json(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    url = f"{_base_url()}{path}"
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=_timeout_s()) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body.strip() else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LM Studio HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"LM Studio nicht erreichbar unter {_base_url()}: {exc}") from exc


def _is_chat_model(model_id: str) -> bool:
    lowered = model_id.lower()
    return not any(hint in lowered for hint in EMBED_HINTS)


def list_model_ids() -> list[str]:
    payload = _http_json("GET", "/v1/models")
    models = payload.get("data", [])
    return [str(item["id"]) for item in models if isinstance(item, dict) and "id" in item]


def resolve_model_id(preferred: str | None = None) -> str:
    if preferred:
        return preferred
    env_model = os.environ.get("LMSTUDIO_MODEL")
    if env_model:
        return env_model
    chat_models = [mid for mid in list_model_ids() if _is_chat_model(mid)]
    if not chat_models:
        raise RuntimeError("Kein Chat-Modell in LM Studio gefunden (nur Embeddings?).")
    for candidate in chat_models:
        if "codestral" in candidate.lower() or "qwen" in candidate.lower():
            return candidate
    return chat_models[0]


def chat_completion(
    *,
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> str:
    model_id = resolve_model_id(model)
    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    response = _http_json("POST", "/v1/chat/completions", payload)
    choices = response.get("choices", [])
    if not choices:
        raise RuntimeError(f"Leere LM-Studio-Antwort: {response!r}")
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(f"Ungültige Modellantwort: {response!r}")
    return content.strip()


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        parsed = json.loads(match.group(0))
        if isinstance(parsed, dict):
            return parsed
    raise ValueError(f"Kein JSON-Objekt in Modellantwort: {text[:400]}...")


REVIEW_SYSTEM = """Du bist eine kritische Erst-Review-Instanz für Code, Pläne und technische Entscheidungen.
Analysiere den Inhalt gründlich und unabhängig.
Antworte ausschließlich als JSON-Objekt (kein Markdown, kein Fließtext):
{
  "preliminary_verdict": "approved|rejected|needs_changes",
  "risk_level": "low|medium|high",
  "findings": ["..."],
  "rationale": "...",
  "required_changes": ["..."]
}"""

CONFIRM_SYSTEM = """Du bist eine unabhängige Zweitinstanz zur Bestätigung einer Erstbewertung.
Du erhältst Originalinhalt und die Erstbewertung — prüfe, ob die Erstbewertung nachvollziehbar ist.
Sei skeptisch bei vorschnellem APPROVED bei riskantem Inhalt.
Antworte ausschließlich als JSON-Objekt (kein Markdown, kein Fließtext):
{
  "confirmed": true,
  "final_verdict": "approved|rejected|needs_changes",
  "rationale": "...",
  "dissent": "...",
  "confidence": 0.0
}"""


@dataclass
class ReviewSession:
    review_id: str
    subject: str
    content: str
    context: str
    created_at: float
    model_primary: str
    model_confirm: str | None = None
    primary_review: dict[str, Any] | None = None
    confirmation: dict[str, Any] | None = None
    confirmed: bool = False
    final_verdict: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)


class ReviewStore:
    def __init__(self) -> None:
        self._sessions: dict[str, ReviewSession] = {}
        self._lock = threading.Lock()

    def create(self, session: ReviewSession) -> ReviewSession:
        with self._lock:
            self._sessions[session.review_id] = session
        return session

    def get(self, review_id: str) -> ReviewSession:
        with self._lock:
            session = self._sessions.get(review_id)
        if session is None:
            raise KeyError(f"Review-Session nicht gefunden: {review_id}")
        return session

    def update(self, session: ReviewSession) -> None:
        with self._lock:
            self._sessions[session.review_id] = session


REVIEW_STORE = ReviewStore()


def run_primary_review(
    *,
    subject: str,
    content: str,
    context: str = "",
    model: str | None = None,
) -> tuple[ReviewSession, dict[str, Any]]:
    model_id = resolve_model_id(model or os.environ.get("LMSTUDIO_REVIEW_MODEL"))
    user_prompt = (
        f"Betreff: {subject}\n\n"
        f"Kontext:\n{context or '(keiner)'}\n\n"
        f"Zu prüfender Inhalt:\n{content}"
    )
    raw = chat_completion(
        messages=[
            {"role": "system", "content": REVIEW_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        model=model_id,
        temperature=0.15,
    )
    parsed = _extract_json_object(raw)
    session = ReviewSession(
        review_id=str(uuid.uuid4()),
        subject=subject,
        content=content,
        context=context,
        created_at=time.time(),
        model_primary=model_id,
        primary_review=parsed,
        final_verdict=str(parsed.get("preliminary_verdict", "needs_changes")),
    )
    REVIEW_STORE.create(session)
    return session, parsed


def _normalize_confirmation(
    primary: dict[str, Any],
    confirmation: dict[str, Any],
) -> dict[str, Any]:
    """Verhindert widersprüchliche final_verdict/confirmed-Kombinationen."""
    confirmed = bool(confirmation.get("confirmed", False))
    primary_verdict = str(primary.get("preliminary_verdict", "needs_changes"))
    dissent = str(confirmation.get("dissent", "")).strip()
    final = str(confirmation.get("final_verdict", primary_verdict))

    if not confirmed:
        if final == "approved":
            final = "needs_changes"
    elif not dissent:
        final = primary_verdict
    elif final == "approved" and primary_verdict in {"rejected", "needs_changes"}:
        final = primary_verdict

    confirmation = dict(confirmation)
    confirmation["confirmed"] = confirmed
    confirmation["final_verdict"] = final
    return confirmation


def run_confirmation_review(
    session: ReviewSession,
    *,
    model: str | None = None,
) -> tuple[ReviewSession, dict[str, Any]]:
    if session.primary_review is None:
        raise RuntimeError("Erstbewertung fehlt — zuerst review_analyze ausführen.")
    model_id = resolve_model_id(
        model or session.model_confirm or os.environ.get("LMSTUDIO_CONFIRM_MODEL") or session.model_primary
    )
    user_prompt = (
        f"Betreff: {session.subject}\n\n"
        f"Originalinhalt:\n{session.content}\n\n"
        f"Kontext:\n{session.context or '(keiner)'}\n\n"
        f"Erstbewertung (JSON):\n{json.dumps(session.primary_review, ensure_ascii=False, indent=2)}"
    )
    raw = chat_completion(
        messages=[
            {"role": "system", "content": CONFIRM_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        model=model_id,
        temperature=0.1,
    )
    parsed = _extract_json_object(raw)
    parsed = _normalize_confirmation(session.primary_review, parsed)
    session.model_confirm = model_id
    session.confirmation = parsed
    session.confirmed = bool(parsed.get("confirmed", False))
    session.final_verdict = str(parsed.get("final_verdict", session.final_verdict or "needs_changes"))
    REVIEW_STORE.update(session)
    return session, parsed


def _session_summary(session: ReviewSession) -> dict[str, Any]:
    return {
        "review_id": session.review_id,
        "subject": session.subject,
        "model_primary": session.model_primary,
        "model_confirm": session.model_confirm,
        "primary_review": session.primary_review,
        "confirmation": session.confirmation,
        "confirmed": session.confirmed,
        "final_verdict": session.final_verdict,
        "created_at": session.created_at,
    }


def build_mcp_server():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(
        "lmstudio-review",
        instructions=(
            "LM-Studio-MCP mit zweistufigem Review: "
            "review_analyze → review_confirm. "
            "Optional review_full für beides in einem Schritt."
        ),
    )

    @mcp.tool()
    def lmstudio_status() -> str:
        """Prüft LM Studio und listet verfügbare Modelle."""
        models = list_model_ids()
        chat_models = [m for m in models if _is_chat_model(m)]
        active = resolve_model_id()
        payload = {
            "base_url": _base_url(),
            "reachable": True,
            "model_count": len(models),
            "chat_models": chat_models,
            "active_model": active,
            "review_model_env": os.environ.get("LMSTUDIO_REVIEW_MODEL"),
            "confirm_model_env": os.environ.get("LMSTUDIO_CONFIRM_MODEL"),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @mcp.tool()
    def lmstudio_list_models() -> str:
        """Listet alle LM-Studio-Modell-IDs."""
        return json.dumps(list_model_ids(), ensure_ascii=False, indent=2)

    @mcp.tool()
    def lmstudio_chat(
        prompt: str,
        system: str = "Du bist ein hilfreicher Assistent.",
        model: str = "",
        temperature: float = 0.3,
    ) -> str:
        """Direkter Chat mit LM Studio (OpenAI-kompatibel)."""
        reply = chat_completion(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            model=model or None,
            temperature=temperature,
        )
        return reply

    @mcp.tool()
    def review_analyze(
        subject: str,
        content: str,
        context: str = "",
        model: str = "",
    ) -> str:
        """Erst-Review-Instanz: kritische Erstbewertung, speichert review_id für review_confirm."""
        session, primary = run_primary_review(
            subject=subject,
            content=content,
            context=context,
            model=model or None,
        )
        return json.dumps(
            {
                "stage": "primary",
                "review_id": session.review_id,
                "model": session.model_primary,
                "primary_review": primary,
                "next_step": "review_confirm aufrufen mit review_id",
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.tool()
    def review_confirm(review_id: str, model: str = "") -> str:
        """Zweit-Review-Instanz: bestätigt oder widerlegt die Erstbewertung."""
        session = REVIEW_STORE.get(review_id)
        session, confirmation = run_confirmation_review(session, model=model or None)
        return json.dumps(
            {
                "stage": "confirmation",
                "review_id": session.review_id,
                "confirmed": session.confirmed,
                "final_verdict": session.final_verdict,
                "primary_review": session.primary_review,
                "confirmation": confirmation,
                "summary": _session_summary(session),
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.tool()
    def review_full(
        subject: str,
        content: str,
        context: str = "",
        model: str = "",
        confirm_model: str = "",
    ) -> str:
        """Vollständiger zweistufiger Review (Erstinstanz + Bestätigung) in einem Aufruf."""
        session, primary = run_primary_review(
            subject=subject,
            content=content,
            context=context,
            model=model or None,
        )
        session, confirmation = run_confirmation_review(
            session,
            model=confirm_model or None,
        )
        return json.dumps(
            {
                "stage": "full",
                "review_id": session.review_id,
                "confirmed": session.confirmed,
                "final_verdict": session.final_verdict,
                "primary_review": primary,
                "confirmation": confirmation,
                "models": {
                    "primary": session.model_primary,
                    "confirm": session.model_confirm,
                },
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.tool()
    def review_get(review_id: str) -> str:
        """Liest eine gespeicherte Review-Session."""
        session = REVIEW_STORE.get(review_id)
        return json.dumps(_session_summary(session), ensure_ascii=False, indent=2)

    return mcp


def main(argv: list[str] | None = None) -> int:
    _configure_logging()
    parser = argparse.ArgumentParser(description="LM Studio MCP Server für Cursor")
    parser.add_argument(
        "--check",
        action="store_true",
        help="LM Studio Erreichbarkeit prüfen (kein MCP)",
    )
    sub = parser.add_subparsers(dest="command")

    review_parser = sub.add_parser("review", help="Review-Workflow per CLI testen")
    review_parser.add_argument("--subject", required=True)
    review_parser.add_argument("--file", type=Path, help="Dateiinhalt als Review-Input")
    review_parser.add_argument("--content", default="", help="Inline-Inhalt")
    review_parser.add_argument("--context", default="")
    review_parser.add_argument("--model", default="")
    review_parser.add_argument("--confirm-model", default="")

    args = parser.parse_args(argv)

    if args.check:
        try:
            payload = {
                "base_url": _base_url(),
                "models": list_model_ids(),
                "active_model": resolve_model_id(),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        except RuntimeError as exc:
            print(f"FEHLER: {exc}", file=sys.stderr)
            return 1

    if args.command == "review":
        content = args.content
        if args.file is not None:
            content = args.file.read_text(encoding="utf-8")
        if not content.strip():
            print("FEHLER: --file oder --content erforderlich", file=sys.stderr)
            return 2
        session, primary = run_primary_review(
            subject=args.subject,
            content=content,
            context=args.context,
            model=args.model or None,
        )
        session, confirmation = run_confirmation_review(
            session,
            model=args.confirm_model or None,
        )
        print(
            json.dumps(
                {
                    "review_id": session.review_id,
                    "confirmed": session.confirmed,
                    "final_verdict": session.final_verdict,
                    "primary_review": primary,
                    "confirmation": confirmation,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    mcp = build_mcp_server()
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
