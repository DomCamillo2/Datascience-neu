"""Metrics for agreement between two automatic annotators."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

from .config import UPOS_TAGS


def normalize_upos(label: str) -> str:
    lab = (label or "").strip().upper()
    return lab if lab in UPOS_TAGS else "OTHER"


def normalize_lemma(lemma: str) -> str:
    if lemma is None or (isinstance(lemma, float) and pd.isna(lemma)):
        return ""
    return str(lemma).strip().lower()


def upos_accuracy(first: pd.Series, second: pd.Series) -> float:
    """Raw UPOS agreement; neither input is a gold-standard reference."""
    first_n = first.map(normalize_upos)
    second_n = second.map(normalize_upos)
    return float((first_n == second_n).mean())


def lemma_accuracy(first: pd.Series, second: pd.Series) -> float:
    """Raw lemma-string agreement; neither input is a gold-standard reference."""
    return float((first.map(normalize_lemma) == second.map(normalize_lemma)).mean())


def cohen_kappa(first: pd.Series, second: pd.Series) -> float:
    """Chance-corrected UPOS agreement between two automatic annotators."""
    return float(
        cohen_kappa_score(first.map(normalize_upos), second.map(normalize_upos))
    )


def bootstrap_agreement(
    sent_ids: pd.Series,
    correct: pd.Series,
    n_boot: int = 1000,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Observed token agreement and a sentence-resampled 95% bootstrap CI."""
    df = pd.DataFrame({"sent_id": sent_ids, "correct": correct.astype(bool)})
    if df.empty:
        raise ValueError("Cannot bootstrap an empty set of annotations.")

    groups = [
        group["correct"].to_numpy(dtype=float)
        for _, group in df.groupby("sent_id", sort=False)
    ]
    rng = np.random.default_rng(seed)
    stats = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        chosen = rng.integers(0, len(groups), size=len(groups))
        stats[i] = np.concatenate([groups[j] for j in chosen]).mean()

    observed = float(df["correct"].mean())
    return (
        observed,
        float(np.quantile(stats, 0.025)),
        float(np.quantile(stats, 0.975)),
    )


def permutation_agreement_baseline(
    first: pd.Series,
    second: pd.Series,
    n_perm: int = 1000,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Chance agreement distribution after independently shuffling one tag sequence."""
    first_n = first.map(normalize_upos).to_numpy()
    second_n = second.map(normalize_upos).to_numpy()
    if len(first_n) != len(second_n) or len(first_n) == 0:
        raise ValueError("Inputs must be non-empty and have equal length.")

    rng = np.random.default_rng(seed)
    stats = np.empty(n_perm, dtype=float)
    for i in range(n_perm):
        stats[i] = (first_n == rng.permutation(second_n)).mean()
    return (
        float(stats.mean()),
        float(np.quantile(stats, 0.025)),
        float(np.quantile(stats, 0.975)),
    )
