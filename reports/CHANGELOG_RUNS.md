# Run log & change notes

Living lab notebook for what we tried, what broke, and what changed.  
**Keep appending** — do not rewrite history silently.

Team: Dominik Soballa, Luca Bouché · Course: Data Science for Linguists (SoSe 2026)

---

## Topic evolution (framing)

| When | Framing | Why changed |
|------|---------|-------------|
| Early | Grambank side-harmony (GB024×GB025) | Solid typology, felt “boring” for a 1,0 push |
| Mid | L1 SpaCy vs LLM on Kafka | Teammate concern: sounds like **model bake-off**, not linguistics |
| **Locked 2026-08-04** | **Linguistic loci of automatic annotation disagreement** (Kafka DE/EN) | Language Use / corpus practice; SpaCy+LLM = instruments only |

Locked RQ: Which UPOS categories show strongest SpaCy↔LLM disagreement, and does the profile differ DE vs EN?  
Hypotheses: H1 uneven loci · H2 DE≠EN profiles · H3 agreement ≫ chance, ≪ ceiling.

---

## Environment locks

| Item | Value |
|------|--------|
| Python | 3.11 (uv venv in `project/.venv`; system 3.9 too old for current SpaCy) |
| SpaCy | 3.8.x · models `de_core_news_md`, `en_core_web_md` |
| LLM | Ollama **`llama3.2:3b`**, temperature **0** |
| Sample | 300 sents / language, seed **42** |
| Design rule | SpaCy tokenizes; LLM must **not** re-tokenize (1:1 `tok_id`) |
| Hardware | Mac M4 Pro (~24 GB) — fine for local Ollama |
| GitHub | https://github.com/DomCamillo2/Datascience-neu |

Also present locally (not used for main runs): `gemma4:12b`.

---

## Annotation / analysis trial runs

### Run 0 — Smoke (DE only)
- **When:** 2026-08-04 (prep phase)
- **What:** Minimal Ollama call via client; cache `data/processed/llm_cache/_smoke_de.json`
- **Result:** OK — API + JSON path works
- **Artifact:** `_smoke_de.json` (tracked)

### Run 1 — Pilot `--limit 5`
- **When:** 2026-08-04 evening (prep)
- **Command:** `python scripts/run_llm_annotate.py --limit 5`
- **Result:** DE+EN annotated; **100% parse_ok** (pilot)
- **Artifacts:** early `annotations_{de,en}.csv` (later overwritten by Run 2)
- **Check:** `python scripts/check_prep.py` → all OK

### Run 2 — Trial `--limit 15` (implementability test)
- **When:** 2026-08-04 ~22:13–22:16 CEST
- **Command:** `python scripts/run_llm_annotate.py --limit 15`
- **Duration:** DE ~103s · EN ~47s
- **Result:**

| Lang | Sents | Parse-OK sents | Tokens | UPOS agree* | Lemma* |
|------|------:|---------------:|-------:|------------:|-------:|
| DE | 15 | 14/15 (93%) | 496 | **64.3%** | 51.4% |
| EN | 15 | 15/15 (100%) | 315 | **68.9%** | 82.2% |

\*parse_ok tokens only

- **Top loci (trial, unstable n):** PART / SCONJ / AUX / CCONJ / ADV (function-word heavy)
- **Failure:** DE `sent_id=65` → `No JSON list found in model output` (cached as `parse_ok=false`; batch continued)
- **Post-analysis bug (fixed):** analysis script used wrong column names (`spacy_upos` vs `upos_spacy`) → first smoke analysis crashed after successful annotate
- **Second bug (fixed):** `normalize_lemma` crashed on NaN LLM lemmas → hardened in `src/metrics.py`
- **Artifacts:**
  - `data/processed/annotations_{de,en}.csv` (15-sent trial state)
  - `data/processed/llm_cache/{de,en}/sent_*.json` (15 each)
  - `reports/TRIAL_RUN.md`

### Run 3 — Full 300+300
- **Status:** **not started**
- **Command:** `python scripts/run_llm_annotate.py` (Ollama.app open; resumable)
- **Note:** Current CSVs are **trial-sized**; full run will extend/overwrite via cache

---

## Bugs & fixes log

| # | Issue | Fix | File(s) |
|---|--------|-----|---------|
| 1 | System Python 3.9 incompatible with SpaCy | uv + Python 3.11 venv | `.venv/` |
| 2 | Risk of LLM re-tokenization | Fixed SpaCy token list → JSON labels by `tok_id` | `src/ollama_client.py`, `src/prompt_template.md` |
| 3 | Trial analysis `KeyError: spacy_upos` | Use real columns `upos_spacy` / `upos_llm` | analysis one-liner → documented |
| 4 | `normalize_lemma` on NaN | Treat NaN/None as `""` | `src/metrics.py` |
| 5 | Occasional LLM non-JSON | Cache fail + continue; resume/retry later | `scripts/run_llm_annotate.py` |
| 6 | Stale notebook stub `03_agreement.md` | Point to `03_loci_analysis.ipynb` | `notebooks/03_agreement.md` |

---

## Repo / tooling changes (chronological highlights)

Git commits on `main` (project repo):

| Commit | Summary |
|--------|---------|
| `b7f7d76` | Initial Grambank side-harmony scaffold |
| `ca844a2` | Retarget → L1 SpaCy vs LLM on Kafka |
| `24dbc15` | Reframe → **linguistic loci** (Language Use) |
| `e50b6fc` | Track SpaCy samples + smoke cache |
| `faf6313` | Prep complete: annotator, notebooks, env pins, pilot |
| `14b66a2` | `AGENTS.md` + notebook stub routing |
| `a94fdd7` | Full lecture/assignment **markdown corpus** for LLMs |

Other local (workspace) work not all on GitHub history:

- Built `llm_corpus/` from all Vorlesungenslides PDFs (every page) + assignment sheets/solutions
- Rebuild scripts: `scripts/rebuild_llm_corpus.py`, `rebuild_assignments_md.py`
- Cursor rule `.cursor/rules/course-llm-corpus.mdc`, root `AGENTS.md` / `llms.txt`
- Copied cleaned `llm_corpus/` into published project repo (raw dumps gitignored)

---

## Design decisions logged

1. **Instruments not objects:** never lead with “which model wins.”
2. **One frozen LLM** for main runs (`llama3.2:3b`); no multi-model cook-off.
3. **Resumable cache** per sentence under `data/processed/llm_cache/{lang}/`.
4. **Report narrative:** category loci + DE vs EN profiles first; overall agreement secondary (H3).
5. **Course MD corpus** is LLM source of truth; PDFs optional locally.

---

## Open / next

- [ ] Full annotation 300+300
- [ ] Retry failed DE `sent_65` (delete cache file then re-run, or dedicated retry)
- [ ] Notebook 03 loci analysis on full data + bootstrap
- [ ] Notebook 04 report
- [ ] Submit proposal ≤ **31 Aug 2026**
- [ ] Invite Dellert on GitHub

---

## How to append

When you run something new, add a subsection under **Annotation / analysis trial runs** with: date, command, n, parse_ok, key metrics, failures, artifacts.  
When you change code/framing, add a row to **Bugs & fixes** or **Repo / tooling**.

---

## Agent onboarding (2026-08-04)

Future LLMs must start at repo-root [`AGENTS.md`](../AGENTS.md) (full brief) and [`llms.txt`](../llms.txt) (pointer). Cursor always-apply rule: `.cursor/rules/agents-brief.mdc`.


### Repository relocation and wording alignment — 2026-08-19
- Current repository: https://github.com/DomCamillo2/Datascience-neu
- Documentation now describes **inter-annotator disagreement**, not annotation unreliability or model error without a human gold standard.
- DE/EN contrasts are framed as differences between the German text and English translation corpus versions, not as general language effects.


### Pipeline validation and analysis notebook — 2026-08-19
- Fixed sentence bootstrap resampling: duplicated sampled sentences now contribute repeatedly, so the CI is a valid sentence-level bootstrap.
- Added token-ID and JSON-object validation for LLM output; malformed or reordered labels now fail instead of being silently aligned by list position.
- Added the --retry-failed flag to re-query cached failed LLM annotations.
- Implemented notebook 03 for per-UPOS loci, confusion pairs, overall agreement, Cohen's kappa, and a permutation-based chance baseline.
