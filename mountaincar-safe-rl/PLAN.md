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
