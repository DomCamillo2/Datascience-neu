# Project Proposal (Draft)

**Title:** Linguistic loci of automatic annotation disagreement in literary German and English: Kafka’s *Trial*  
**Course:** Data Science for Linguists, Summer 2026  
**Instructor:** Johannes Dellert  
**Contributors:** Dominik Soballa, Luca Bouché  
**Registration track:** Language Use  
**Deadline (proposal):** 31 August 2026  
**Deadline (project):** 31 December 2026 (default)

---

## 1. Introduction and research question

Corpus-based linguistics depends on **automatic annotation** (part of speech, lemmas). Literary language—here Franz Kafka’s *Der Prozess* / *The Trial*—differs from the news-like registers many tools are associated with. When two independent automatic annotators disagree, the interesting question for linguists is not “which system wins,” but **where in the grammar** disagreement concentrates, and whether that profile **differs between the German and English corpus versions**.

We use **SpaCy** and a **frozen local LLM** as two automatic annotators on the same tokens. Neither is treated as ground truth: disagreement marks **loci of inter-annotator disagreement** (ambiguity, domain effects, morphology, naming, etc.). Without human gold labels, it does not establish which system is wrong or that annotation is unreliable.

**Research question:**  
In a literary Kafka corpus, which **linguistic categories** (UPOS; secondarily lemmas) show the strongest automatic-annotation disagreement between SpaCy and an LLM—and does this **disagreement profile** differ between the German and English corpus versions?

---

## 2. Objective

1. Build token-aligned automatic annotations (SpaCy + LLM) on sampled DE/EN Kafka sentences.  
2. Quantify overall disagreement / agreement as a baseline (not as a model contest).  
3. Map **linguistic loci** of disagreement (per UPOS; top confusion pairs) — primary scientific contribution.  
4. Contrast the German vs English corpus-version disagreement profiles.  
5. Report uncertainty (bootstrap over sentences) and limitations for corpus practice.

---

## 3. Preliminary literature and resources

**Course anchors**

- Session 04 / Assignment 03: SpaCy on these Kafka texts (`de_core_news_md`, `en_core_web_md`)  
- Session 11: resampling / uncertainty  
- Session 12: Language Use = corpus linguistics; reproducibility; proposal fidelity  

**Background themes**

- Literary / narrative NLP and domain shift (e.g. literary German pipeline evaluations such as LLpro-related work)  
- POS annotation difficulty and scheme/category effects (UD evaluation discussions)  
- LLMs as additional automatic annotators — used here as a **second independent label source**, not as the research object  

**Data**

- `kafka_1925_der-prozess.txt`, `kafka_1925_the-trial.txt` (course / Project Gutenberg materials)

---

## 4. Scope

### In scope

- Literary German Kafka text + English Kafka translation samples  
- Two automatic annotators: SpaCy (course models) + one pinned local LLM (Ollama `llama3.2:3b`, temperature 0)  
- Primary analysis: **UPOS disagreement by category** and **DE vs EN profile contrast**  
- Secondary: lemma string agreement  
- Sample ~300 sentences/language (seed 42); fixed SpaCy tokenization  
- Metrics: category-wise disagreement rates, confusion pairs, overall agreement/κ as summary, bootstrap CIs  

### Out of scope

- Declaring a “better” model or leaderboard-style bake-off as the main claim  
- Human gold annotation  
- Dependencies, NER, sentiment, fine-tuning  
- Full-novel commercial API runs  

**Reasons:** align with Language Use / corpus questions; keep methods valid (1:1 token alignment); time budget.

---

## 5. Hypotheses

- **H1 (loci):** Disagreement is **uneven across UPOS categories**—higher for categories often hard in literary text (e.g. PROPN, AUX/VERB, ambiguous open-class items) than for closed-class / punctuation.  
- **H2 (corpus-version contrast):** The **category-wise disagreement profile** differs between the German text and the English translation. This is interpreted as a contrast between these corpus versions, not proof of a general language effect.  
- **H3 (baseline):** Overall token agreement is above chance but below ceiling—confirming non-trivial but structured disagreement rather than random noise.

---

## 6. Methodology

### Data preparation

- Load texts; newlines → spaces (Assignment 03).  
- SpaCy sentence split + tokenization; sample sentences; export token tables.

### Second annotator (LLM)

- **SpaCy tokens are fixed.** LLM returns one UPOS (+ lemma) per token index (JSON).  
- No free re-tokenization. Invalid tags → `OTHER` (reported).

### Analysis (linguistic emphasis)

1. Per-UPOS disagreement rates and confusion pairs (**H1**)  
2. Compare DE vs EN corpus-version category profiles (**H2**)  
3. Overall agreement/κ + bootstrap CIs as summary (**H3**)  
4. Qualitative examples of disagreement with linguistic commentary  

### Collaboration

Dominik Soballa and Luca Bouché work jointly on all parts; equal shared responsibility.

---

## 7. Preliminary week plan

| Period | Work |
|--------|------|
| Aug (→ 31) | Finalize & submit proposal |
| Sep | SpaCy samples frozen; start LLM annotation |
| Oct | Full annotation; loci analysis + DE/EN contrast |
| Nov | Report notebook (linguistic interpretation) + packaging |
| Dec | Buffer / supervisor feedback |

Amendments to methods require a short written note before changing the graded deliverable.

---

## 8. Expected outcomes

- A **map of linguistic loci** where automatic annotators diverge in literary DE/EN Kafka.  
- Evidence whether the German and English corpus versions show **different disagreement profiles**.  
- Practical takeaway: which categories deserve additional caution in coarse literary corpus counts.

**If overall agreement is high:** loci analysis may still reveal residual hard categories—still a valid result.  
**If agreement is low:** we interpret structured vs unstructured disagreement and discuss domain/morphology—not “LLM failed.”

**Interpretation limit:** The English data are a translation. DE/EN contrasts are therefore reported as corpus-version differences, not as general language effects.

---

## Sign-off

Contributors: Dominik Soballa / Luca Bouché Date: _________  
Submitted to supervisor: _________ Feedback received: _________
