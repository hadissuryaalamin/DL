# Audit log — `paper/main.tex` → `paper/main_draft.tex`

**Date:** 2026-06-14
**Auditor:** Claude (review session 6)
**Scope:** Post-"P4 rescue" flaw audit of the paper, and the edits applied to produce
`paper/main_draft.tex`. Source of truth for verdicts: `review/report.md`,
`review/stage2_p4_300_summary.md`, `results/stage2_p4_300_summary.md`, and the implementation
(`src/agents/safe_ppo.py`, `src/envs.py`, `src/buffers.py`).

**Overall verdict:** After the P4 rescue the paper is *internally sound and free of
contradictions* — every number reconciles with the summaries and `report.md`, the code matches
Algorithm 1 and Eqs (4)–(5), and the central thesis is correctly downgraded to a fixed-compute
screening rule. The remaining issues were presentation/rigor, not correctness; they are addressed
in `main_draft.tex` (left as a separate file for review before replacing `main.tex`).

---

## Findings and actions

| # | Severity | Location (main.tex) | Finding | Action in main_draft.tex |
|---|---|---|---|---|
| 1 | should-fix | line 182 | Budget conversion written as `≈ d/0.53`; `report.md` and the load-bearing arithmetic `15/0.52 ≈ 29` use **0.52**. | Changed `d/0.53` → `d/0.52`. |
| 2 | should-fix | Discussion (rescue ¶), lines 400/431–433 | The **central rescued finding (S19–S24) had no figure or table** — prose-only — while every lesser result has both. `review/stage2_p4_150_vs_300.png` exists but was referenced nowhere. | Added **Table `tab:p4300`** (S13–S18 vs S19–S24: 150-cost, 300-cost, return, pass) and a `\tabref` to it in the rescue paragraph. Chose a compact table over the PNG to save space and avoid copying a figure into `paper/figures/`. |
| 3 | should-fix | lines 95–97, 139 | "potential-style" shaping overclaimed policy-invariance. `envs.py` adds φ(s)=1.5·\|x−(−0.5)\| **directly** (+100 terminal bonus) → not Ng et al. 1999 potential shaping; it changes the objective. The recommended speed/cost-tension observation was also absent. | Reworded Related Work and Method 4.1 to state plainly it is **non-potential**, modifies the objective, and is identical for every agent (comparisons internally consistent, not policy-invariant). Added one sentence to the Discussion noting the height bonus *encourages* the very speed the cost penalizes (shaping ↔ constraint tension). |
| 4 | minor | lines 216, 221–225, 400 | Units mismatch was acknowledged but never *connected to why P4 is the borderline base* (P4's cost ≈29 ≈ effective episode budget d/0.52 ≈ 29 → P4 starts on the zero-gradient threshold). | Added that mechanistic link to the rescue paragraph, tying the units footnote to the central finding. |
| 5 | should-fix | Tables 1/3; Limitations line 415 | All reported numbers are **stochastic training-rollout** statistics (never disclosed); argmax/deterministic is consistently safer; S6/S12 selection is within seed noise. | Limitations: added item (iii) disclosing stochastic-rollout numbers (deterministic is safer → numbers understate safety); softened item (i) to "S6 was the only config meeting both criteria *under this three-seed protocol* (S6/S12 gap within seed noise)". |
| 6 | resolved — no change | lines 67–73, 89–93, 172 | Novelty framing already correct: dual-critic placed in the PPO-Lagrangian family, Ray et al. 2019 / Stooke et al. 2020 cited, framed as a case study. (Residual "novelty" wording lives only in `src/` comments and `CLAUDE.md`, not the paper.) | None. |
| 7 | resolved — no change | Alg. 1 box; Eqs (4)/(5) | Verified line-by-line against `safe_ppo.py` (clipped reward obj, unclipped −λ·cost obj, +entropy; Ĵ_C = mean(R̂^C); dual-ascent direction) and `buffers.py` (cost-adv scale-only, zeroed on zero-cost batch). No mismatch. | None. |

### Not addressed (deferred — reviewer awareness)
- **Deterministic (argmax) evaluation table** (`review/deterministic_eval.md`) is referenced only via the
  new Limitations sentence, not added as a results table — out of scope/space for this pass.
- **Five-seed confirmation** remains pending; already acknowledged in Limitations (i).
- `results/safe_S6/` has **no checkpoint**, so the winner cannot be deterministically evaluated without
  retraining (repo hygiene item, noted in `report.md` §7).

---

## Page-limit compliance (8 pages)

Target: **≤ 8 pages excluding references.** The edits above (esp. the new table) pushed the original
8-page layout to 9. Compression applied so the body + Conclusion fit on 8 pages and **page 9 contains
references only**:

- Shortened the **Conclusion** (it duplicated the abstract).
- Compressed the **P4 rescue paragraph** and made **Table `tab:p4300`** compact (`\small`,
  merged the S13→S19 ID columns, dropped the all-`1.00` Solved column into the caption).
- Trimmed the **abstract's** redundant P4 passage.
- Reduced figure widths: feasibility probe 0.52→0.44, Stage-1 0.50→0.43, Stage-2 scatter
  0.56→0.47, winner dynamics 0.85→0.72, learning curves 0.52→0.45 `\linewidth`.

Result (verified via `pdfinfo`): 8 content pages; page 9 = references [7]–[13] only. Compile is clean
(no undefined references or citations).

---

## Files

- `paper/main_draft.tex` — edited draft (this audit's output). Diff vs `paper/main.tex`.
- `review/p4_rescue_explainer.html` — companion plain-language walkthrough of the P4 rescue
  (background, mechanism, fix, and how it strengthens the report).
- `review/audit_main_draft.md` — this log.

To adopt: review `main_draft.tex`, then `mv paper/main_draft.tex paper/main.tex` and recompile
(`pdflatex → bibtex → pdflatex ×2`).
