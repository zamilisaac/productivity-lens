---
name: pl-classify
description: Productivity Lens initiative classifier. Separates real productivity initiatives from everything else (sustainability, HR benefits, revenue, acquisitions, plans, scale) the same way every time. Claude answers six fixed fact questions (F1–F6) per initiative from the quote; a tested script applies Playbook Module 2A to decide counted / not counted, Tier, Grade, Evidence type, lesson and headline eligibility, and flags conflicts for Decisions. Use this whenever running EXTRACT, ANALYSE, FULL, RUN, REDO, audit Step 3 (re-apply the productivity test), whenever an Initiative Inventory or "Not counted" sheet is made or changed, whenever the Playbook or Rules tab changes, and whenever anyone asks whether something counts as a productivity initiative. Use it instead of labelling initiatives by judgement.
---

# pl-classify — the productivity test, applied by code

Why: labelling an initiative in one go (pass/fail, Tier, Grade, Evidence type) lets small rules slip, and
the same item gets different labels on different days. Here Claude only answers **facts** that can be
checked against the quote; `scripts/classify.py` turns the facts into labels with the Playbook rules.
When the Playbook changes, only the script changes and the stored answers are re-run (no re-reading reports).

Needs `openpyxl` (`pip install openpyxl`).

## 1. List every candidate (EXTRACT, no judgement yet)

Put **every** activity the report describes that could be an initiative in the answers file – including ones
that will clearly fail (CSR, solar, training hours, acquisitions, plans). Template:
`templates/Initiative_answers_template.csv`. One row per initiative, with the verbatim `quote`, printed
`page` (pl-evidence) and `source` (`AR`, `SR` = only in the sustainability pages, or `both`).

## 2. Answer F1–F6 for each row

Read `references/rubric.md` first. For each row fill `category`, `status`, `result_kind`, `input`, `figure`,
`area` from the closed lists, using only what the quote says.
- Not sure, or two values fit → `uncertain = Y` and a short `uncertain_reason`. Never guess.
- A Rules-tab rule settles it → `rule` (e.g. `R008`) and `rule_outcome` (`pass`/`fail`). The script records it.
- Fill `reported_result` with the figures you will show; the script checks they are in the quote.

## 3. Run the engine

```bash
python scripts/classify.py run "<...>/[Code]_[Name]_FY[YYYY]_Answers.csv" \
  --out "<...>/[Code]_[Name]_FY[YYYY]_Initiatives.xlsx"
```
Output workbook: **Initiatives** (counted, Playbook columns + lesson/headline eligibility), **Not counted**
(with the reason), **Decisions** (uncertain items, quote conflicts, lesson candidates with warnings),
**Answers** (the facts, for REDO). Plus `…summary.json` (counts, fail reasons, `enough_for_story`).

If `enough_for_story` is false (fewer than three lesson-eligible items), read the FY-2 then FY-4 reports
(Playbook 2A, "Earlier reports") and add their initiatives to the same answers file.

## 4. Second check for items that will be shown

For every row the engine marks `lesson_eligible = Y` or with a `headline_role`, answer F1–F6 again in a
**separate pass** (a fresh subagent given only the rubric, initiative name and quote – not the first answers).
Save as `…_Answers_check.csv` with the same `id`s, then:
```bash
python scripts/classify.py compare first_answers.csv second_answers.csv
```
Any disagreement that changes a label (`=> counted/tier/grade/evidence_type/lesson_eligible`) goes to
Decisions with both answers. Fact-only disagreements that change no label need no decision.

## 5. Decisions and Rules

Items in the Decisions sheet go to the decision gate (Playbook "Decisions"). Each answer the user gives
becomes a Rules-tab rule **and** is written back to the answers file (`rule`, `rule_outcome`, or a
corrected fact), so the next run gives the same result without asking again.

## 6. Test the engine before every Playbook or rubric change

```bash
python tests/test_classify.py                                        # engine unit tests + Playbook examples
python scripts/classify.py test tests/playbook_examples.csv --min 100
python scripts/classify.py test "<private gold set>.csv" --min 95    # user-approved labels (kept in Drive)
```
A gold set is an answers file with `expected_counted`, `expected_tier`, `expected_grade`,
`expected_evidence_type` columns, filled from labels the user has approved. Real gold sets contain draft
company judgements: keep them in Drive or `private/` (git-ignored), never in the public repo.
Every mismatch is either an engine bug (fix the script), a rubric gap (fix `rubric.md`), or a wrong
expected label (ask the user).

## REDO

A Playbook change never needs the reports re-read: update `classify.py` (and the tests), then re-run
`classify.py run` on the stored Answers sheet. Only rows whose labels change need human attention.
