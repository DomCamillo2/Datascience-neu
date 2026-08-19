#!/usr/bin/env python3
"""Batch-annotate fixed SpaCy token samples with Ollama (resumable)."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ollama_client import DEFAULT_MODEL, annotate_tokens  # noqa: E402


def _validate_labels(labels: list[dict], tokens: list[str]) -> None:
    if len(labels) != len(tokens):
        raise ValueError(f"Cached length mismatch: {len(labels)} labels for {len(tokens)} tokens")
    for i, label in enumerate(labels):
        if not isinstance(label, dict) or label.get("tok_id") != i:
            raise ValueError(f"Cached token alignment mismatch at position {i}")


def _failed_labels(tokens: list[str]) -> list[dict]:
    return [
        {
            "tok_id": i,
            "upos": "X",
            "lemma": token,
            "upos_norm": "OTHER",
            "upos_valid": False,
        }
        for i, token in enumerate(tokens)
    ]


def annotate_language(
    lang: str,
    limit: int | None,
    model: str,
    retry_failed: bool,
) -> Path:
    sample_path = ROOT / "data" / "processed" / f"tokens_{lang}_sample.csv"
    cache_dir = ROOT / "data" / "processed" / "llm_cache" / lang
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_path = ROOT / "data" / "processed" / f"annotations_{lang}.csv"

    df = pd.read_csv(sample_path)
    sent_ids = sorted(df["sent_id"].unique())
    if limit is not None:
        sent_ids = sent_ids[:limit]

    rows: list[dict] = []
    n_ok = 0
    n_fail = 0
    t0 = time.time()

    for i, sid in enumerate(sent_ids, 1):
        cache_file = cache_dir / f"sent_{sid}.json"
        sent = df.loc[df["sent_id"] == sid].sort_values("tok_id")
        tokens = sent["token"].astype(str).tolist()
        spacy_upos = sent["upos"].astype(str).tolist()
        spacy_lemma = sent["lemma"].astype(str).tolist()

        parse_ok = True
        err = ""
        labels: list[dict] = []
        use_cache = cache_file.exists()

        if use_cache:
            payload = json.loads(cache_file.read_text(encoding="utf-8"))
            parse_ok = bool(payload.get("parse_ok", False))
            err = str(payload.get("error", ""))
            labels = payload.get("labels", [])
            if not parse_ok and retry_failed:
                use_cache = False
            elif parse_ok:
                try:
                    _validate_labels(labels, tokens)
                except ValueError as exc:
                    parse_ok = False
                    err = str(exc)
                    use_cache = False

        if not use_cache:
            try:
                labels = annotate_tokens(tokens, model=model, temperature=0.0)
                _validate_labels(labels, tokens)
                parse_ok = True
                err = ""
            except Exception as exc:  # noqa: BLE001 — batch continues and is resumable
                parse_ok = False
                err = str(exc)
                labels = _failed_labels(tokens)
            cache_file.write_text(
                json.dumps(
                    {
                        "sent_id": int(sid),
                        "parse_ok": parse_ok,
                        "labels": labels,
                        "error": err,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

        if parse_ok:
            n_ok += 1
        else:
            n_fail += 1

        for j, token in enumerate(tokens):
            label = labels[j]
            rows.append(
                {
                    "language": lang,
                    "sent_id": int(sid),
                    "tok_id": j,
                    "token": token,
                    "upos_spacy": spacy_upos[j],
                    "lemma_spacy": spacy_lemma[j],
                    "upos_llm": label["upos"],
                    "lemma_llm": label["lemma"],
                    "upos_llm_norm": label["upos_norm"],
                    "parse_ok": parse_ok,
                    "error": err,
                }
            )

        if i % 10 == 0 or i == len(sent_ids):
            elapsed = time.time() - t0
            print(
                f"[{lang}] {i}/{len(sent_ids)} sents | ok={n_ok} fail={n_fail} | {elapsed:.0f}s",
                flush=True,
            )

    pd.DataFrame(rows).to_csv(out_path, index=False)
    rate = n_ok / max(len(sent_ids), 1)
    print(f"[{lang}] wrote {out_path} rows={len(rows)} parse_ok_rate={rate:.1%}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["de", "en", "both"], default="both")
    parser.add_argument("--limit", type=int, default=None, help="Max sentences per language")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Re-query cached sentences whose previous annotation failed",
    )
    args = parser.parse_args()

    for lang in (["de", "en"] if args.lang == "both" else [args.lang]):
        annotate_language(lang, args.limit, args.model, args.retry_failed)


if __name__ == "__main__":
    main()
