"""Ollama HTTP client for token-aligned UPOS/lemma annotation."""

from __future__ import annotations

import json
import re
from typing import Any

import requests

from .config import UPOS_TAGS
from .metrics import normalize_upos

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3.2:3b"

PROMPT_TEMPLATE = """You are a linguistic annotator.
You receive a JSON list of tokens in order.
Return ONLY a JSON list of the same length (no markdown, no commentary).
Each item must be an object:
  {{"tok_id": <int>, "upos": <UD UPOS tag>, "lemma": <string>}}
Use only these UPOS tags:
ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X
Do not add, remove, or split tokens.

Tokens:
{tokens_json}
"""


def _extract_json_list(text: str) -> list[Any]:
    text = text.strip()
    fence = chr(96) * 3
    if text.startswith(fence):
        text = re.sub(rf"^{re.escape(fence)}(?:json)?\s*", "", text)
        text = re.sub(rf"\s*{re.escape(fence)}$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start < 0 or end < 0:
        raise ValueError("No JSON list found in model output")
    items = json.loads(text[start : end + 1])
    if not isinstance(items, list):
        raise ValueError("Model output must be a JSON list")
    return items


def annotate_tokens(
    tokens: list[str],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
    timeout: int = 120,
) -> list[dict[str, Any]]:
    """Return validated, position-aligned annotations for the supplied token list."""
    payload_tokens = [{"tok_id": i, "token": t} for i, t in enumerate(tokens)]
    prompt = PROMPT_TEMPLATE.format(tokens_json=json.dumps(payload_tokens, ensure_ascii=False))
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    items = _extract_json_list(resp.json().get("response", ""))
    if len(items) != len(tokens):
        raise ValueError(f"Length mismatch: got {len(items)} labels for {len(tokens)} tokens")

    out: list[dict[str, Any]] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item {i} is not a JSON object")
        try:
            returned_id = int(item["tok_id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Item {i} has no valid tok_id") from exc
        if returned_id != i:
            raise ValueError(
                f"Token alignment mismatch at position {i}: model returned tok_id={returned_id}"
            )

        raw_upos = str(item.get("upos", "")).strip().upper()
        if not raw_upos:
            raise ValueError(f"Item {i} has no UPOS label")
        lemma = str(item.get("lemma", tokens[i]))
        out.append(
            {
                "tok_id": i,
                "upos": raw_upos,
                "lemma": lemma,
                "upos_norm": normalize_upos(raw_upos),
                "upos_valid": raw_upos in UPOS_TAGS,
            }
        )
    return out
