# Project Plan: MountainCar Safe RL

Detailed task breakdown for transforming `MountainCar_main.ipynb` into a reproducible
3-phase project with paper and demonstration videos.

**Convention:**
- `[x]` done in sandbox / committed in repo
- `[~]` partially done (single-seed only, awaiting local multi-seed re-run)
- `[ ]` pending — must be executed locally (sandbox cannot install PyTorch)

---

## Phase A — Refactor & codebase (DONE in sandbox)

**Goal:** turn the monolithic notebook into a modular, reproducible Python package.

| # | Task | Status | Output |
|---|---|---|---|
| A.1 | Create folder skeleton (`src/`, `scripts/`, `configs/`, `notebooks/`, `results/`, `videos/`, `paper/`) | `[x]` | `mountaincar-safe-rl/` |
| A.2 | Extract environment wrappers into `src/envs.py` | `[x]` | `ShapedMountainCar`, `ConstrainedMountainCar` |
| A.3 | Extract network architectures into `src/networks.py` | `[x]` | `QNetwork`, `PPONetwork`, `SafePPONetwork` |
| A.4 | Extract replay/rollout buffers into `src/buffers.py` | `[x]` | `DQNReplayBuffer`, `PPORolloutBuffer`, `SafePPORolloutBuffer` |
| A.5 | Build DQN trainer in `src/agents/dqn.py` with `@dataclass` config | `[x]` | `DQNAgent`, `train_dqn(seed, cfg, log_dir)` |
| A.6 | Build PPO trainer in `src/agents/ppo.py` | `[x]` | `train_ppo(seed, cfg, log_dir)` |
| A.7 | Build Safe PPO trainer in `src/agents/safe_ppo.py` (Phase 3 novelty) | `[x]` | `train_safe_ppo(seed, cfg, log_dir)` |
| A.8 | Add `src/utils.py` with `set_seed`, JSON IO, dir helpers | `[x]` | `set_seed`, `save_json`, `load_json` |
| A.9 | Write CLI scripts `run_dqn.py`, `run_ppo.py`, `run_safe_ppo.py`, `run_all.py` | `[x]` | `--seed`, `--config`, `--out` flags |
| A.10 | Write YAML configs per algorithm | `[x]` | `configs/{dqn,ppo,safe_ppo}.yaml` |
| A.11 | Pin dependencies in `requirements.txt` | `[x]` | gymnasium, torch, scipy, pyyaml, matplotlib, imageio, pygame |
| A.12 | Syntax-check all modules with `ast.parse` | `[x]` | 14/14 files OK |

---

## Phase B — Multi-seed training runs (LOCAL execution)

**Goal:** generate `metrics.json` for 3 seeds × 3 algorithms with full per-step logging.

**Why local:** the sandbox cannot fit `torch + CUDA` deps (~6 GB) into its 1.5 GB free disk.
The notebook already ran on your machine, so PyTorch + Gymnasium are installed there.

| # | Task | Status | Command |
|---|---|---|---|
| B.1 | (Bootstrap) Parse seed_0 metrics from notebook outputs | `[x]` | already in `results/{algo}/seed_0/metrics.json` |
| B.2 | Run DQN seeds 0, 1, 2 (~3 × 2.5 min = 7.5 min) | `[ ]` | `python -m scripts.run_dqn --seed 0` … |
| B.3 | Run PPO seeds 0, 1, 2 (~3 × 18 min = 54 min) | `[ ]` | `python -m scripts.run_ppo --seed 0` … |
| B.4 | Run Safe PPO seeds 0, 1, 2 (~3 × 15 min = 45 min) | `[ ]` | `python -m scripts.run_safe_ppo --seed 0` … |
| B.5 | OR run everything in one shot | `[ ]` | `python -m scripts.run_all --seeds 0 1 2` |
| B.6 | Verify each `results/<algo>/seed_<s>/metrics.json` has full per-epoch arrays | `[ ]` | `python -c "import json; print(len(json.load(open('results/safe_ppo/seed_0/metrics.json'))['epoch_returns']))"` |

**Expected total wall time:** ~1h 45min on CPU. GPU not required.

---

## Phase C — Analysis & paper figures (PARTIAL: single-seed, awaits B)

**Goal:** generate paper-quality figures with mean ± std bands across seeds.

| # | Task | Status | Output |
|---|---|---|---|
| C.1 | Write `notebooks/analysis.py` that loads `results/*/seed_*/metrics.json` and computes mean ± std | `[x]` | falls back to single-seed if only seed_0 exists |
| C.2 | Generate Figure 1: DQN learning curve | `[~]` | `paper/figures/fig1_dqn_curve.pdf` (seed_0 only) |
| C.3 | Generate Figure 2: PPO learning curve | `[~]` | `paper/figures/fig2_ppo_curve.pdf` (seed_0 only) |
| C.4 | Generate Figure 3: 3-way return comparison vs env steps | `[~]` | `paper/figures/fig3_comparison_return.pdf` |
| C.5 | Generate Figure 4: Safe PPO dual-axis return + cost | `[~]` | `paper/figures/fig4_safe_ppo_dual.pdf` |
| C.6 | Generate Figure 5: Lagrangian λ trajectory | `[~]` | `paper/figures/fig5_lambda_trajectory.pdf` |
| C.7 | Generate Figure 6: cost curve vs budget | `[~]` | `paper/figures/fig6_cost_curve.pdf` |
| C.8 | Re-run `analysis.py` after Phase B to regenerate with error bands | `[ ]` | `python notebooks/analysis.py` |
| C.9 | Update Table 1 in paper with multi-seed mean ± std | `[ ]` | edit `paper/main.tex` lines 280–296 |

---

## Phase D — Video deliverables (NEW: side-by-side comparison)

**Goal:** produce a single MP4 showing DQN, PPO, and Safe~PPO playing `MountainCar`
simultaneously in three side-by-side panels, with per-panel annotations.

**Requires:** Phase B completed (need trained checkpoints `qnet.pt`, `ppo_net.pt`, `safe_ppo_net.pt`).

| # | Task | Status | Detail |
|---|---|---|---|
| D.1 | Copy existing notebook videos to `videos/` | `[x]` | `dqn_training_live.mp4`, `dqn_mountaincar.mp4`, `dqn_training_progress.mp4` |
| D.2 | Write `scripts/make_comparison_video.py` (split-screen renderer) | `[x]` (next step) | loads 3 checkpoints, renders 3-panel MP4 |
| D.3 | Define video layout: 3 panels horizontal, 200 px label strip above each | spec | total canvas ~1800×450 px (3 × 600×400 + headers) |
| D.4 | Annotation per panel: algorithm name, episode, step, reward, (cost+λ for Safe PPO) | spec | drawn on each frame via PIL |
| D.5 | Synchronization: each agent resets at the same env-frame index; if one finishes early its panel freezes on final frame | spec | step-locked rendering loop |
| D.6 | Run `python scripts/make_comparison_video.py --episodes 3` | `[ ]` | produces `videos/comparison_3algo.mp4` |
| D.7 | (Optional) Add a constraint-violation overlay (red flash when `|v| > 0.04` for Safe PPO panel) | `[ ]` | feature in `make_comparison_video.py` |

**Estimated output:** ~5–15 sec MP4 per episode, 3 episodes = ~30–45 sec clip.

---

## Phase E — Paper (NeurIPS-style LaTeX) (DONE, awaits multi-seed update)

| # | Task | Status | Output |
|---|---|---|---|
| E.1 | Write `paper/main.tex`: Abstract, Intro, Related Work, Background, Method, Experiments, Results, Discussion, Conclusion | `[x]` | 7 pages |
| E.2 | Write Algorithm 1 (Safe PPO pseudo-code) inline | `[x]` | minipage-based, no `algorithm.sty` dependency |
| E.3 | Write `paper/references.bib` with 12 references (DQN, PPO, GAE, CPO, CMDP, PPO-Lagrangian, PID-Lagrangian, reward shaping, etc.) | `[x]` | `references.bib` |
| E.4 | Compile to PDF with `pdflatex → bibtex → pdflatex × 2` | `[x]` | `paper/main.pdf` (349 KB) |
| E.5 | Re-compile after Phase C.8 to pick up multi-seed figures | `[ ]` | `cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` |
| E.6 | Switch to official NeurIPS style file if submitting (uncomment `\usepackage[final]{neurips_2024}`) | `[ ]` | requires `neurips_2024.sty` |

---

## Phase F — Reproducibility & polish (PARTIAL)

| # | Task | Status | Output |
|---|---|---|---|
| F.1 | Write `README.md` with setup, structure, reproduce, build instructions | `[x]` | `README.md` |
| F.2 | Add `.gitignore` for `__pycache__`, LaTeX aux, `.pt` checkpoints | `[x]` | `.gitignore` |
| F.3 | Verify all Python modules pass `ast.parse` syntax check | `[x]` | 14/14 OK |
| F.4 | Verify `analysis.py` runs end-to-end with current seed_0 data | `[x]` | generates 6 PDFs |
| F.5 | Verify LaTeX compiles from scratch | `[x]` | `main.pdf` builds clean |
| F.6 | (After Phase B) Smoke-test `scripts.run_all --seeds 0` locally to confirm fresh install works | `[ ]` | local task |
| F.7 | (Optional) Add `pytest` smoke tests for envs, networks, buffers | `[ ]` | future work |
| F.8 | (Optional) Git tag the version, add CITATION.cff | `[ ]` | publishing prep |

---

## Critical path to "fully done"

These are the only steps blocking completion — everything else is already in place:

1. **On your local machine:**
   ```bash
   cd E:\DL\mountaincar-safe-rl
   pip install -r requirements.txt           # ensure deps fresh
   python -m scripts.run_all --seeds 0 1 2   # ~1h 45min
   python scripts/make_comparison_video.py   # ~5 min
   python notebooks/analysis.py              # regen figures with bands
   cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
   ```

2. **Manual edit** of Table 1 in `paper/main.tex` (lines 280–296) to insert multi-seed mean ± std numbers from `results/<algo>/seed_{0,1,2}/metrics.json`.

3. **(Optional)** Polish: switch to official `neurips_2024.sty`, write CITATION.cff.

Total active human time: ~30 min (most of the wall time is unattended training).

---

## Time / resource budget

| Phase | Where | Wall time | Disk |
|---|---|---|---|
| A | sandbox | done | < 1 MB |
| B (multi-seed) | local | ~1h 45min | < 50 MB |
| C (re-plot) | local | < 1 min | < 5 MB |
| D (video) | local | ~5 min | ~30 MB |
| E (re-compile) | local | < 1 min | < 1 MB |

**Sandbox limitations encountered:** 1.5 GB free disk cannot fit PyTorch + CUDA wheels
(~6 GB). All ML training therefore offloaded to local. Sandbox is still useful for code
authoring, LaTeX builds, plot regeneration, and any non-torch analysis.

---
---

# Part 2 — Safe PPO Experiment Plan (PPO-Lagrangian)

> Goal: find a configuration that satisfies the constraint (avg cost <= 15) without
> return collapse. Approach: **first determine whether the constraint is feasible**,
> then stabilize the base PPO, then search for the safety setting.
> Consolidated from `RL_experiment_plan.md` (v1) + `RL_experiment_plan_v2.md` (v2).
> v2 fully supersedes v1; the content below is v2. Saved: 2026-06-05.

## What changed from v1 (and why)
This revision was written after reading the code (`src/envs.py`, `src/agents/safe_ppo.py`,
`configs/safe_ppo.yaml`). Four important points that were not explicit before:

1. **Cost is proportional, not a step count.** In `ConstrainedMountainCar`:
   `cost = (|v| - 0.04) * 100` when `|v| > 0.04`, otherwise 0. MountainCar speed
   is capped at ±0.07, so the maximum cost per step = `(0.07-0.04)*100 = 3.0`.
   "avg cost <= 15" = average total cost per episode <= 15.
2. **The structural tension is computable, and tight.** To solve, the car must reach
   ~0.07. Each step at peak speed = cost 3. That means a budget of 15 is only enough
   for ~5 steps at peak speed (or more steps at moderate speed). This is narrow — so
   **feasibility must be checked first**, not assumed.
3. **Lambda bug confirmed.** The old code updated lambda with
   `loss_lambda = -exp(log_lambda) * (cost - cost_limit)`, so the gradient w.r.t.
   `log_lambda` was also multiplied by `exp(log_lambda)=lambda`. When lambda is small
   (config `log_lambda_init=-3.0` -> lambda~0.05), lambda barely moves =
   self-suppression. The fix below removes this factor (see the Mandatory fixes section).
4. **Cost metric inconsistency.** Lambda is updated using the **discounted** cost
   return (`ret_c.mean()`), but what is reported/checked against the limit is the
   **undiscounted** episode cost (`ep_ret_c`). Two different quantities. They must be
   reconciled before the experiment, otherwise "passes the constraint" is ambiguous
   (see Mandatory fix #2).

## Principles
- At each stage vary only the 2 highest-impact axes; freeze the rest.
- 3 seeds per combination for screening; **5 seeds for finalists** (B1-B3 and the
  Stage 2 winner) because std from 3 samples is not reliable.
- The lambda-update bug is fixed first as a CONSTANT (not an experiment variable).
- Reported return and cost are read from a **separate deterministic evaluation**
  (see Evaluation protocol), not from the rollout batch used for the update.

## Mandatory fixes before starting (fix, not gridded)

**#1 — Lambda update rule to avoid self-suppression.**
Replace the lambda update block in `safe_ppo.py` (`update()`):

```python
with torch.no_grad():
    violation = (actual_batch_cost - cost_limit) / cost_limit  # normalized
    log_lambda += lam_lr * violation       # without the exp factor
    log_lambda.clamp_(min=-2.0, max=3.0)   # floor & ceiling -> lambda in [~0.135, ~20]
lam = torch.exp(log_lambda)
```

Note on the floor consequence: `min=-2.0` means lambda never drops below ~0.135, so
there is always a small "tax" on return even when the constraint is already safe.
That is intentional (to prevent lambda from dying entirely), but be aware that Stage 2
return will never match Stage 1 return (see Reading the results).

**#2 — Use the same cost quantity for both the update and the reporting.**
Pick one definition and use it consistently:
- Recommendation: use the **undiscounted episode cost** (`ep_ret_c`, the same one
  reported) for the lambda update too — so that the "avg cost <= 15" being checked is
  exactly what is optimized. If you keep using the discounted cost for the update,
  report both numbers in the table and declare which one is the pass condition.

**#3 — Log feasibility diagnostics each epoch.**
The code already stores `epoch_violations` (number of steps with cost > 0) and
`epoch_costs`. Also add, for **solved** episodes, the distribution of their cost
(min/mean). This is used in Stage 0 and for interpretation.

---

## STAGE 0 — Feasibility probe (run this first)
Goal: answer "is there a trajectory that solves WITH cost <= 15?" before spending
dozens of runs. Cheap: ~2-4 runs.

How: take 1 base PPO that already solves (or the output of `run_ppo.py`), then
- measure the distribution of **cost per episode on solved episodes** (not the average
  over all episodes), or
- run Safe PPO with a **large fixed lambda** (e.g. lambda=10, no update) for a few
  epochs and see where `avg_cost` converges while `solved_rate` stays > 0.

Decision:

| Probe result | Interpretation | Proceed to |
|--------------|----------------|------------|
| cost-min of solved episodes <= 15 (consistent) | feasible, purely a tuning problem | STAGE 1 then 2, as is |
| cost-min of solved episodes > 15 (consistent) | infeasible, no lambda can save it | "If infeasible" section |
| solving disappears entirely under large lambda | the constraint kills the ability to solve | "If infeasible" section |

Write the probe results here before continuing:
- cost-min of solved episodes (mean+-std across episodes): ____
- solved_rate at lambda=10: ____
- Feasibility conclusion: ____

---

## STAGE 1 — Base PPO (Lagrangian lambda = 0)
Vary: lr x ent_coef. Goal: a base that CAN solve + is STABLE, and record its cost too.
Fixed: gamma=0.99, clip=0.2, lam_gae=0.95, steps=4000, epochs=150,
target_kl~0.015, lr_critic=1e-3, ent default via shaping (height bonus + 100 goal bonus active).

| ID | lr   | ent_coef | Return(mean+-std) | Avg cost (info) | Collapse?(seed) | Stable? | Top-3? |
|----|------|----------|-------------------|-----------------|-----------------|---------|--------|
| P1 | 1e-4 | 0.0      |                   |                 |                 |         |        |
| P2 | 1e-4 | 0.01     |                   |                 |                 |         |        |
| P3 | 3e-4 | 0.0      |                   |                 |                 |         |        |
| P4 | 3e-4 | 0.01     |                   |                 |                 |         |        |
| P5 | 1e-3 | 0.0      |                   |                 |                 |         |        |
| P6 | 1e-3 | 0.01     |                   |                 |                 |         |        |

### Base-selection change (important)
- **Record avg cost in Stage 1 even though lambda=0.** High return on this task = solve =
  speed ~0.07 = high cost. Picking a base from return alone = picking the base that
  violates the constraint the most, then dragging it into Stage 2 as the worst possible
  starting point.
- **Top-3 = bases that solve with the best selection score**, where score =
  `mean_return - std_return` (an explicit rule, not eyeballing), AND cost is not
  extreme. If two bases tie on return, pick the one with lower cost.
- Mark them B1, B2, B3.

### Exploration & gamma note (conditional unfreeze)
- Reward shaping is already active (height bonus + 100 goal bonus), so exploration is
  not as sparse as plain MountainCar. The grid `ent_coef in {0, 0.01}` can be used as is.
- **If >= 4 of the 6 combinations fail to solve**, don't fiddle with lr first. Unfreeze
  one axis in priority order: (1) gamma 0.99 -> 0.999 (effective horizon of
  gamma=0.99 ~100 steps, episode 200 steps), (2) ent_coef to 0.05. Record this change
  as a deviation.

---

## STAGE 2 — Safe PPO on top of the top-3
Vary: lam_lr x log_lambda_init. cost_limit=15 (fixed). Update rule already fixed (#1, #2).

| ID  | Base | lam_lr | log_lambda_init | Avg cost(<=15?) | Return(mean+-std) | lambda final | Collapse? | Pass? |
|-----|------|--------|-----------------|-----------------|-------------------|--------------|-----------|-------|
| S1  | B1   | 0.02   | -1.0            |                 |                   |              |           |       |
| S2  | B1   | 0.02   |  0.0            |                 |                   |              |           |       |
| S3  | B1   | 0.03   | -1.0            |                 |                   |              |           |       |
| S4  | B1   | 0.03   |  0.0            |                 |                   |              |           |       |
| S5  | B1   | 0.05   | -1.0            |                 |                   |              |           |       |
| S6  | B1   | 0.05   |  0.0            |                 |                   |              |           |       |
| S7  | B2   | 0.02   | -1.0            |                 |                   |              |           |       |
| S8  | B2   | 0.02   |  0.0            |                 |                   |              |           |       |
| S9  | B2   | 0.03   | -1.0            |                 |                   |              |           |       |
| S10 | B2   | 0.03   |  0.0            |                 |                   |              |           |       |
| S11 | B2   | 0.05   | -1.0            |                 |                   |              |           |       |
| S12 | B2   | 0.05   |  0.0            |                 |                   |              |           |       |
| S13 | B3   | 0.02   | -1.0            |                 |                   |              |           |       |
| S14 | B3   | 0.02   |  0.0            |                 |                   |              |           |       |
| S15 | B3   | 0.03   | -1.0            |                 |                   |              |           |       |
| S16 | B3   | 0.03   |  0.0            |                 |                   |              |           |       |
| S17 | B3   | 0.05   | -1.0            |                 |                   |              |           |       |
| S18 | B3   | 0.05   |  0.0            |                 |                   |              |           |       |

Note: the `lam_lr` range {0.02, 0.03, 0.05} is narrow (2.5x). If the lambda dynamics
(see Reading the results) show lambda too sluggish / too wild across the whole grid,
switch the range to {0.01, 0.03, 0.1} rather than adding rows. `log_lambda_init` may be
a low-impact axis; if odd vs. even S* results are nearly the same across all bases, init
can be fixed to -1.0 and that axis replaced with something else.

### Evaluation protocol (applies to Stage 1 & 2)
- Return and avg cost for the **table** are read from a **deterministic** evaluation
  (argmax action) over >= 20 episodes, separate from the training rollout.
- lambda final = the lambda value at the end of training (average of the last 10 epochs).

### Measurable definitions (remove eyeballing)
- **Collapse** = return drops > 30% from the peak value ever reached AND does not
  recover to >= 90% of the peak within the last 20 epochs. (Adjust the 30% if needed,
  but set it BEFORE reading the results.)
- **Stable** = no collapse on any of the three seeds.
- **Pass** = avg cost <= 15 (on the metric chosen in #2) AND no collapse.

### Reading the results
- Avg cost <= 15 = the primary condition for passing the constraint.
- Return = compare against the base return in Stage 1 (how much was sacrificed).
  Remember the lambda floor: even a "safe" run will be slightly below the base return.
- lambda final = sanity check: cost still >15 but lambda small -> raise lam_lr;
  lambda explodes (hits the ~20 ceiling) + return collapses -> lower lam_lr.
- Large lambda oscillation = consider damping (see Technical notes), don't immediately
  blame the lam_lr value.
- **Final winner** = the Pass row with the highest mean return and smallest std;
  re-run the winner with 5 seeds before claiming it final.

---

## If infeasible — principled relaxation (from Stage 0)
If Stage 0 shows there is no solving trajectory with cost <= 15, DO NOT run the Stage 2
grid (54 runs that will certainly fail). Pick a relaxation, ordered from most honest:

1. **Raise cost_limit** to slightly above the cost-min-feasible from Stage 0. The limit
   should be derived from the task physics, not a number set in advance.
2. **Raise the `max_speed` threshold** from 0.04 closer to what the task requires. If the
   point of the cost is "don't speed unnecessarily", 0.04 penalizes speed that is in fact
   required to solve.
3. **Redefine cost**: penalize only unnecessary high speed (e.g. outside the
   momentum-building phase), not every fast step.
4. **Report as a Pareto front**: sweep cost_limit {12, 15, 20, 25} and show the
   return-vs-cost curve. If there is no "safe AND solve" point, that curve is itself a
   valid and honest result.

---

## Technical notes (optional, for diagnosis)
- The lambda update is currently a pure P-controller (gradient ascent). Prone to
  oscillation. If lambda swings hard, use PID-Lagrangian (add integral/derivative terms)
  or lower lam_lr; this is not a grid variable, only a fix if the problem appears.
- Check the scale: lambda ceiling ~20 vs. reward scale (shaping + 100 bonus). If
  `lambda * cost` dominates the reward, collapse is not about tuning but about scale.

## Experiment budget
- Stage 0: ~2-4 runs (gating, mandatory first)
- Stage 1: 6 combinations x 3 seeds = 18 runs (+ 5-seed rerun of finalists)
- Stage 2: 18 combinations x 3 seeds = 54 runs (+ 5-seed rerun of the winner)
- Total ~ 76-80 runs, BUT Stage 2 only runs if Stage 0 = feasible.

## Honest note
The 0.04 speed threshold fights the task's requirement (it needs ~0.07 to reach the
goal), and because cost is proportional, a budget of 15 only allows ~5 steps at peak
speed. That is why Stage 0 (feasibility probe) comes first: if return drops on all seeds
after the fix, that is a signal of structural tension — relax the cost_limit/threshold
via the "If infeasible" section, rather than continuing to tune lambda.
