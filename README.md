# Linguistic loci of annotation disagreement (Kafka DE/EN)

**Team:** Dominik Soballa, Luca Bouché  
**Course:** Data Science for Linguists (SoSe 2026)  
**Track:** Language Use  

## What this project is

A **corpus-linguistics** study of where two automatic POS/lemma annotation systems disagree in literary German and English Kafka texts, and whether those **disagreement loci** differ between the two corpus versions.

Two automatic annotation systems are compared on the same tokenized material; the scientific interest is in **where disagreement concentrates**, not in a leaderboard. Without human gold labels, disagreement is not evidence that either system is wrong.

## What it is not

A model bake-off or a “which tagger is better?” project.

## Project docs

| What | Where |
|------|--------|
| Course instructions | [`AGENTS.md`](AGENTS.md) |
| Short pointer | [`llms.txt`](llms.txt) |
| Topic lock | [`PLAN.md`](PLAN.md) |
| Proposal draft | [`proposal/PROPOSAL_DRAFT.md`](proposal/PROPOSAL_DRAFT.md) |
| Implementation plan | [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) |
| Status / checklist | [`reports/PREP_STATUS.md`](reports/PREP_STATUS.md) |
| Change log | [`reports/CHANGELOG_RUNS.md`](reports/CHANGELOG_RUNS.md) |
| Course slides / markdown corpus | [`llm_corpus/INDEX.md`](llm_corpus/INDEX.md) |

## Status

- [x] Raw Kafka texts  
- [x] SpaCy samples (300 sentences/language)  
- [x] Prep scripts + notebooks 01–04  
- [x] Small second-annotator validation run  
- [ ] Full second-annotator run (300 sentences/language)  
- [ ] Loci analysis DE/EN  
- [ ] Report + proposal submit  

See [`reports/PREP_STATUS.md`](reports/PREP_STATUS.md).

## Immediate next steps

1. Freeze the data and validation pipeline for the seed-42 sample sentences.
2. Run the full DE and EN comparison annotation on the fixed sample.
3. Compute disagreement rates by UPOS and compare the German and English corpus-version profiles.
4. Build the final notebook narrative around the linguistic loci of disagreement.

## Interpretation note

The English text is a translation. Any DE/EN contrast is therefore described as a difference between these **corpus versions**, not as proof of a general language difference.

## Setup

```bash
source .venv/bin/activate   # Python 3.11 via uv
python scripts/check_prep.py
python scripts/run_llm_annotate.py
```

## GitHub

https://github.com/DomCamillo2/Datascience-neu
