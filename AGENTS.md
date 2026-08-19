# AGENTS.md — instructions for future LLMs / coding agents

**Read this file first** when opening this repository.  
Short pointer: [`llms.txt`](llms.txt) · Course slides: [`llm_corpus/INDEX.md`](llm_corpus/INDEX.md)

| Field | Value |
|-------|--------|
| Course | Data Science for Linguists, Uni Tübingen, SoSe 2026 (Johannes Dellert) |
| Team | Dominik Soballa, Luca Bouché (joint work — no exclusive split) |
| Repo | https://github.com/DomCamillo2/Datascience-neu |
| Track | **Language Use** (corpus linguistics) |
| Proposal due | **31 August 2026** |
| Default project deadline | **31 December 2026** (~90 h/person expected) |

---

## 1. Mandatory read order (do not skip)

1. **This file** (`AGENTS.md`)
2. [`PLAN.md`](PLAN.md) — locked RQ + hypotheses
3. [`reports/CHANGELOG_RUNS.md`](reports/CHANGELOG_RUNS.md) — what was already tried
4. [`reports/PREP_STATUS.md`](reports/PREP_STATUS.md) — checklist / next steps
5. [`reports/MISTAKES.md`](reports/MISTAKES.md) — anti-patterns
6. Only then open code / notebooks for the specific task

For course/lecture questions (not the graded project): start at [`llm_corpus/INDEX.md`](llm_corpus/INDEX.md).

---

## 2. Locked scientific framing (do not reopen without user ask)

### What this project IS

A **corpus-linguistics** study of *where* two automatic POS/lemma annotation systems disagree in **literary** German and English Kafka texts, and whether those **disagreement loci** differ between the two corpus versions.

### What it is NOT

A model leaderboard / “SpaCy vs ChatGPT who wins” bake-off.

### Research question

Which **UPOS** categories show the strongest automatic-annotator disagreement (SpaCy ↔ local LLM), and does this **disagreement profile** differ between German and English?

### Hypotheses

| ID | Claim |
|----|--------|
| H1 | Disagreement is uneven across UPOS (clear loci) |
| H2 | DE vs EN disagreement profiles differ |
| H3 | Overall agreement ≫ chance and ≪ ceiling (structured, not noise) |

### Out of scope (unless proposal amended)

- Claiming which model is “better”
- Human gold annotation as main deliverable
- Dependencies / NER as primary layer
- Fine-tuning / multi-LLM cook-offs
- Treating SpaCy labels as ground truth (they are **annotator A**, not gold)

SpaCy and the LLM are **instruments** that reveal loci of inter-annotator disagreement — not the research object. Without human gold labels, their disagreement does not show which system is wrong.

---

## 3. Hard technical constraints

1. **SpaCy owns tokenization.** LLM must label the given token list 1:1 (`tok_id`). Never let the LLM re-tokenize or freely segment.
2. **Frozen main-run LLM:** Ollama `llama3.2:3b`, temperature **0**. Document any deviation in `reports/CHANGELOG_RUNS.md` and `reports/LLM_CHOICE.md`.
3. **Sample lock:** 300 sentences / language, seed **42** (`data/processed/tokens_{de,en}_sample.csv`). Do not silently resample.
4. **Never edit** `data/raw/` Kafka texts.
5. **Batch runs** via `scripts/run_llm_annotate.py` (resumable per-sentence cache under `data/processed/llm_cache/{lang}/`). Prefer this over ad-hoc notebook loops for full annotation.
6. **Analysis narrative:** lead with **per-UPOS loci** and DE vs EN corpus-version profiles; overall agreement is secondary (supports H3 only). Do not present the DE/EN contrast as proof of a general language effect because the English text is a translation.
7. **Reproducibility (Session 12):** pin requirements, seeds, model IDs, README, raw + transforms. Proposal fidelity is graded — don’t change the promised design quietly.
8. **Append** new trials/fixes to `reports/CHANGELOG_RUNS.md` (do not erase history).

---

## 4. Current status (as of last log update)

See `reports/PREP_STATUS.md` for the live checklist. Snapshot:

| Done | Pending |
|------|---------|
| Topic + proposal draft | Full annotation **300+300** |
| Env (Py3.11, SpaCy DE/EN, Ollama) | Loci analysis notebook 03 on full data |
| Samples 300/lang | Report notebook 04 |
| Prep check all OK | Submit proposal ≤ 31 Aug |
| Pilot (5) + trial (15) runnable | Invite Dellert on GitHub |
| Course `llm_corpus/` markdown in repo | Retry DE fail `sent_65` on full/retry pass |

**Trial (15/lang):** DE UPOS agree ~64% (14/15 parse_ok); EN ~69% (15/15). Top loci: PART/SCONJ/AUX/CCONJ/ADV. Details: `reports/TRIAL_RUN.md`.

**Known issue:** occasional LLM non-JSON → cached `parse_ok=false`; batch continues. Delete that sentence’s cache JSON to retry.

---

## 5. How to run (local)

```bash
cd project   # or repo root if this folder IS the clone root
source .venv/bin/activate          # Python 3.11 via uv
export PATH="$HOME/.local/bin:$PATH"
open -a Ollama                     # keep running for long jobs

python scripts/check_prep.py
python scripts/run_llm_annotate.py --limit 15   # trial
python scripts/run_llm_annotate.py              # full 300+300 (resumable)
```

Annotation CSV columns:  
`language, sent_id, tok_id, token, upos_spacy, lemma_spacy, upos_llm, lemma_llm, upos_llm_norm, parse_ok, error`

Metrics helpers: `src/metrics.py` (`upos_accuracy`, `lemma_accuracy`, `bootstrap_agreement`, `normalize_upos` / `normalize_lemma`).  
**NaN lemmas** must be handled (already hardened in `normalize_lemma`).

---

## 6. Repository map

```
AGENTS.md / llms.txt          ← you are here / short pointer
PLAN.md                       ← topic lock
IMPLEMENTATION_PLAN.md        ← step-by-step execution
proposal/PROPOSAL_DRAFT.md    ← submit to Dellert
reports/                      ← status, trials, mistakes, env, grade rubric
llm_corpus/                   ← ALL lecture slides + assignment sheets as MD
notebooks/                    ← 01 prep · 02 annotate · 03 loci · 04 report
scripts/                      ← check_prep, run_llm_annotate, rebuild_* 
src/                          ← ollama_client, spacy_pipeline, metrics, config
data/raw/                     ← Kafka DE/EN (immutable)
data/processed/               ← samples, annotations, llm_cache
```

### Course corpus (when answering lecture/assignment questions)

| File | Role |
|------|------|
| `llm_corpus/INDEX.md` | Start + lecture table |
| `llm_corpus/COURSE_MAP.md` | Syllabus, goals, project rules |
| `llm_corpus/TOPIC_INDEX.md` | Heading → session router |
| `llm_corpus/lectures/*.md` | Full slide text (every PDF page) |
| `llm_corpus/assignments/exNN.md` | Sheets |
| `llm_corpus/solutions/` | **Only if user asks** for solutions |

Cite YAML `source_pdf` and `<!-- page:N -->`. Do **not** dump entire `ex08_solution.md` into context.

Rebuild from local PDFs (workspace parent `Vorlesungenslides/`):

```bash
.venv/bin/python scripts/rebuild_llm_corpus.py
.venv/bin/python scripts/rebuild_assignments_md.py
```

---

## 7. Do / Don’t (quick)

**Do**

- Lead with linguistic loci and DE vs EN profiles  
- Keep SpaCy token alignment  
- Log every trial in `CHANGELOG_RUNS.md`  
- Prefer `llm_corpus/` markdown over PDFs  
- Preserve proposal fidelity  

**Don’t**

- Reframe as model comparison without explicit user request  
- Change sample seed / model silently  
- Edit raw Kafka texts  
- Add NER/deps/multi-LLM as main work without proposal change  
- Pool DE+EN without separate profiles  
- Skip bootstrap uncertainty on key rates  

---

## 8. Deliverables expected by the course

1. **Proposal** (≤ 31 Aug 2026) — draft in `proposal/PROPOSAL_DRAFT.md`  
2. **Reproducible GitHub project** — invite Dellert  
3. **Notebook narrative** answering H1–H3 with loci maps, DE/EN comparison, limitations  
4. Time budget ~90 h/person; graded on proposal fidelity + scientific quality, not hype  

Grade self-check: [`reports/GRADE_RUBRIC.md`](reports/GRADE_RUBRIC.md)

---

## 9. When the user asks you to continue

1. Read `reports/PREP_STATUS.md` + latest `CHANGELOG_RUNS.md`  
2. State current bottleneck in one sentence  
3. Prefer the next unchecked checklist item (usually: full annotation → notebook 03 → 04 → proposal submit)  
4. After any run or code fix: **append** `CHANGELOG_RUNS.md`  

If workspace is the parent folder `DataScience_Lingo/` (not only this git root), course PDFs/assignments may live one level up; the published GitHub clone is this project tree with `llm_corpus/` included.
