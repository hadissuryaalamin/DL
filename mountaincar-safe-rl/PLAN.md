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

# Part 2 — Rencana Eksperimen Safe PPO (PPO-Lagrangian)

> Tujuan: menemukan konfigurasi yang memenuhi constraint (avg cost <= 15) tanpa
> return collapse. Pendekatan: **tentukan dulu apakah constraint feasible**, baru
> mantapkan base PPO, baru cari setting safety.
> Konsolidasi dari `RL_experiment_plan.md` (v1) + `RL_experiment_plan_v2.md` (v2).
> v2 menggantikan v1 sepenuhnya; isi di bawah adalah v2. Disimpan: 2026-06-05.

## Apa yang berubah dari v1 (dan kenapa)
Revisi ini dibuat setelah membaca kode (`src/envs.py`, `src/agents/safe_ppo.py`,
`configs/safe_ppo.yaml`). Empat hal penting yang sebelumnya tidak eksplisit:

1. **Cost itu proporsional, bukan hitungan step.** Di `ConstrainedMountainCar`:
   `cost = (|v| - 0.04) * 100` saat `|v| > 0.04`, selain itu 0. Kecepatan
   MountainCar dibatasi ±0.07, jadi cost per step maksimum = `(0.07-0.04)*100 = 3.0`.
   "avg cost <= 15" = rata-rata total cost per episode <= 15.
2. **Tension strukturalnya bisa dihitung, dan ketat.** Untuk solve, mobil harus
   menyentuh ~0.07. Tiap step di kecepatan puncak = cost 3. Artinya anggaran 15
   kira-kira hanya cukup untuk ~5 step di kecepatan puncak (atau lebih banyak step
   di kecepatan sedang). Ini sempit — maka **feasibility harus dicek lebih dulu**,
   bukan diasumsikan.
3. **Bug lambda terkonfirmasi.** Kode lama meng-update lambda dengan
   `loss_lambda = -exp(log_lambda) * (cost - cost_limit)`, sehingga gradien
   terhadap `log_lambda` ikut dikali `exp(log_lambda)=lambda`. Saat lambda kecil
   (config `log_lambda_init=-3.0` -> lambda~0.05), lambda nyaris tak bergerak =
   self-suppression. Fix di bawah menghapus faktor ini (lihat bagian Perbaikan wajib).
4. **Inkonsistensi metrik cost.** Lambda di-update memakai **discounted** cost
   return (`ret_c.mean()`), tetapi yang dilaporkan/dicek terhadap limit adalah
   cost episode **undiscounted** (`ep_ret_c`). Dua besaran berbeda. Harus disamakan
   sebelum eksperimen, kalau tidak "lolos constraint" jadi ambigu (lihat Perbaikan wajib #2).

## Prinsip
- Di tiap tahap hanya variasikan 2 sumbu paling berdampak; bekukan sisanya.
- 3 seed per kombinasi untuk screening; **5 seed untuk finalis** (B1-B3 dan
  pemenang Tahap 2) karena std dari 3 sampel tidak reliable.
- Bug update lambda diperbaiki dulu sebagai KONSTAN (bukan variabel eksperimen).
- Return dan cost yang dilaporkan dibaca dari **evaluasi deterministik terpisah**
  (lihat Protokol evaluasi), bukan dari batch rollout yang dipakai update.

## Perbaikan wajib sebelum mulai (fix, bukan di-grid)

**#1 — Update rule lambda agar tidak self-suppression.**
Ganti blok update lambda di `safe_ppo.py` (`update()`):

```python
with torch.no_grad():
    violation = (actual_batch_cost - cost_limit) / cost_limit  # ternormalisasi
    log_lambda += lam_lr * violation       # tanpa faktor exp
    log_lambda.clamp_(min=-2.0, max=3.0)   # floor & ceiling -> lambda in [~0.135, ~20]
lam = torch.exp(log_lambda)
```

Catatan konsekuensi floor: `min=-2.0` berarti lambda tidak pernah turun di bawah
~0.135, jadi selalu ada sedikit "pajak" pada return walau constraint sudah aman.
Itu disengaja (mencegah lambda mati total), tapi sadari return Tahap 2 tidak akan
pernah menyamai return Tahap 1 (lihat Aturan baca hasil).

**#2 — Samakan besaran cost untuk update dan untuk pelaporan.**
Pilih satu definisi dan pakai konsisten:
- Rekomendasi: pakai **cost episode undiscounted** (`ep_ret_c`, sama dengan yang
  dilaporkan) untuk update lambda juga — supaya "avg cost <= 15" yang dicek sama
  persis dengan yang dioptimasi. Kalau tetap pakai discounted untuk update,
  laporkan kedua angka di tabel dan tetapkan mana yang jadi syarat lolos.

**#3 — Catat diagnostik feasibility tiap epoch.**
Kode sudah menyimpan `epoch_violations` (jumlah step ber-cost > 0) dan
`epoch_costs`. Tambahkan juga, untuk episode yang **solved**, distribusi cost-nya
(min/mean). Ini dipakai di Langkah 0 dan untuk interpretasi.

---

## TAHAP 0 — Probe feasibility (jalankan paling dulu)
Tujuan: jawab "apakah ada trajektori yang solve DENGAN cost <= 15?" sebelum
menghabiskan puluhan run. Murah: ~2-4 run.

Cara: ambil 1 base PPO yang sudah solve (atau hasil `run_ppo.py`), lalu
- ukur distribusi **cost per episode pada episode yang solved** (bukan rata-rata
  semua episode), atau
- jalankan Safe PPO dengan **lambda besar tetap** (mis. lambda=10, tanpa update)
  beberapa epoch dan lihat ke mana `avg_cost` konvergen sambil `solved_rate` tetap > 0.

Keputusan:

| Hasil probe | Interpretasi | Lanjut ke |
|-------------|--------------|-----------|
| cost-min episode solved <= 15 (konsisten) | feasible, masalah murni tuning | TAHAP 1 lalu 2, apa adanya |
| cost-min episode solved > 15 (konsisten) | infeasible, tidak ada lambda yang menyelamatkan | Bagian "Kalau infeasible" |
| solve hilang total saat lambda besar | constraint mematikan kemampuan solve | Bagian "Kalau infeasible" |

Tulis hasil probe di sini sebelum lanjut:
- cost-min episode solved (mean+-std antar episode): ____
- solved_rate pada lambda=10: ____
- Kesimpulan feasibility: ____

---

## TAHAP 1 — Base PPO (lambda Lagrangian = 0)
Variasikan: lr x ent_coef. Tujuan: base yang MAMPU solve + STABIL, dan dicatat juga cost-nya.
Fixed: gamma=0.99, clip=0.2, lam_gae=0.95, steps=4000, epochs=150,
target_kl~0.015, lr_critic=1e-3, ent default via shaping (height bonus + 100 bonus goal aktif).

| ID | lr   | ent_coef | Return(mean+-std) | Avg cost (info) | Collapse?(seed) | Stabil? | Top-3? |
|----|------|----------|-------------------|-----------------|-----------------|---------|--------|
| P1 | 1e-4 | 0.0      |                   |                 |                 |         |        |
| P2 | 1e-4 | 0.01     |                   |                 |                 |         |        |
| P3 | 3e-4 | 0.0      |                   |                 |                 |         |        |
| P4 | 3e-4 | 0.01     |                   |                 |                 |         |        |
| P5 | 1e-3 | 0.0      |                   |                 |                 |         |        |
| P6 | 1e-3 | 0.01     |                   |                 |                 |         |        |

### Perubahan seleksi base (penting)
- **Catat avg cost di Tahap 1 walau lambda=0.** Return tinggi di task ini = solve =
  kecepatan ~0.07 = cost tinggi. Memilih base hanya dari return = memilih base yang
  paling melanggar constraint, lalu menyeretnya ke Tahap 2 sebagai titik awal terburuk.
- **Top-3 = base yang solve dengan skor seleksi terbaik**, di mana skor =
  `mean_return - std_return` (aturan eksplisit, bukan penilaian mata), DAN cost tidak
  ekstrem. Kalau dua base setara return, pilih yang cost-nya lebih rendah.
- Tandai B1, B2, B3.

### Catatan exploration & gamma (conditional unfreeze)
- Reward shaping sudah aktif (height bonus + 100 bonus goal), jadi eksplorasi tidak
  sesparse MountainCar polos. Grid `ent_coef in {0, 0.01}` boleh dipakai apa adanya.
- **Jika >= 4 dari 6 kombinasi gagal solve**, jangan utak-atik lr dulu. Unfreeze
  satu sumbu sesuai urutan prioritas: (1) gamma 0.99 -> 0.999 (horizon efektif
  gamma=0.99 ~100 step, episode 200 step), (2) ent_coef ke 0.05. Catat perubahan ini sebagai deviasi.

---

## TAHAP 2 — Safe PPO di atas top-3
Variasikan: lam_lr x log_lambda_init. cost_limit=15 (fixed). Update rule sudah diperbaiki (#1, #2).

| ID  | Base | lam_lr | log_lambda_init | Avg cost(<=15?) | Return(mean+-std) | lambda final | Collapse? | Lolos? |
|-----|------|--------|-----------------|-----------------|-------------------|--------------|-----------|--------|
| S1  | B1   | 0.02   | -1.0            |                 |                   |              |           |        |
| S2  | B1   | 0.02   |  0.0            |                 |                   |              |           |        |
| S3  | B1   | 0.03   | -1.0            |                 |                   |              |           |        |
| S4  | B1   | 0.03   |  0.0            |                 |                   |              |           |        |
| S5  | B1   | 0.05   | -1.0            |                 |                   |              |           |        |
| S6  | B1   | 0.05   |  0.0            |                 |                   |              |           |        |
| S7  | B2   | 0.02   | -1.0            |                 |                   |              |           |        |
| S8  | B2   | 0.02   |  0.0            |                 |                   |              |           |        |
| S9  | B2   | 0.03   | -1.0            |                 |                   |              |           |        |
| S10 | B2   | 0.03   |  0.0            |                 |                   |              |           |        |
| S11 | B2   | 0.05   | -1.0            |                 |                   |              |           |        |
| S12 | B2   | 0.05   |  0.0            |                 |                   |              |           |        |
| S13 | B3   | 0.02   | -1.0            |                 |                   |              |           |        |
| S14 | B3   | 0.02   |  0.0            |                 |                   |              |           |        |
| S15 | B3   | 0.03   | -1.0            |                 |                   |              |           |        |
| S16 | B3   | 0.03   |  0.0            |                 |                   |              |           |        |
| S17 | B3   | 0.05   | -1.0            |                 |                   |              |           |        |
| S18 | B3   | 0.05   |  0.0            |                 |                   |              |           |        |

Catatan: rentang `lam_lr` {0.02, 0.03, 0.05} sempit (2.5x). Kalau dinamika lambda
(lihat Aturan baca hasil) menunjukkan lambda terlalu lamban / terlalu liar di
seluruh grid, ganti rentang jadi {0.01, 0.03, 0.1} ketimbang menambah baris.
`log_lambda_init` mungkin sumbu rendah-dampak; kalau hasil S*-ganjil vs genap nyaris
sama di semua base, init bisa difix ke -1.0 dan sumbu itu diganti hal lain.

### Protokol evaluasi (berlaku Tahap 1 & 2)
- Return dan avg cost untuk **tabel** dibaca dari evaluasi **deterministik**
  (argmax action) atas >= 20 episode, terpisah dari rollout training.
- lambda final = nilai lambda di akhir training (rata-rata 10 epoch terakhir).

### Definisi terukur (hilangkan penilaian mata)
- **Collapse** = return turun > 30% dari nilai puncak yang pernah dicapai DAN tidak
  pulih sampai >= 90% puncak dalam 20 epoch terakhir. (Sesuaikan 30% bila perlu,
  tapi tetapkan SEBELUM membaca hasil.)
- **Stabil** = tidak collapse pada ketiga seed.
- **Lolos** = avg cost <= 15 (pada metrik yang dipilih di #2) DAN tidak collapse.

### Aturan baca hasil
- Avg cost <= 15 = syarat utama lolos constraint.
- Return = bandingkan dengan return base di Tahap 1 (berapa yang dikorbankan).
  Ingat floor lambda: bahkan run "aman" akan sedikit di bawah return base.
- lambda final = sanity check: cost masih >15 tapi lambda kecil -> naikkan lam_lr;
  lambda meledak (mentok ceiling ~20) + return collapse -> turunkan lam_lr.
- Osilasi lambda yang besar = pertimbangkan damping (lihat Catatan teknis), jangan
  langsung salahkan nilai lam_lr.
- **Pemenang akhir** = baris Lolos dengan return mean tertinggi, std terkecil;
  jalankan ulang pemenang dengan 5 seed sebelum diklaim final.

---

## Kalau infeasible — relaksasi yang berprinsip (dari Tahap 0)
Kalau Tahap 0 menunjukkan tidak ada trajektori solve dengan cost <= 15, JANGAN
jalankan grid Tahap 2 (54 run yang pasti gagal). Pilih relaksasi, urut dari paling jujur:

1. **Naikkan cost_limit** ke sedikit di atas cost-min-feasible hasil Tahap 0. Limit
   harusnya turunan dari fisika task, bukan angka yang ditetapkan duluan.
2. **Naikkan ambang `max_speed`** dari 0.04 mendekati nilai yang task butuhkan. Kalau
   tujuan cost adalah "jangan ngebut tanpa perlu", 0.04 menghukum kecepatan yang
   memang wajib untuk solve.
3. **Redefinisi cost**: hukum hanya kecepatan tinggi yang tidak perlu (mis. di luar
   fase membangun momentum), bukan setiap step cepat.
4. **Laporkan sebagai Pareto front**: sweep cost_limit {12, 15, 20, 25} dan tampilkan
   kurva return-vs-cost. Kalau tidak ada titik "aman DAN solve", kurva itu sendiri
   adalah hasil yang valid dan jujur.

---

## Catatan teknis (opsional, untuk diagnosis)
- Update lambda saat ini murni P-controller (gradient ascent). Rawan osilasi. Kalau
  lambda berayun keras, pakai PID-Lagrangian (tambah suku integral/derivatif) atau
  turunkan lam_lr; ini bukan variabel grid, hanya perbaikan kalau muncul masalah.
- Cek skala: lambda ceiling ~20 vs skala reward (shaping + bonus 100). Kalau
  `lambda * cost` mendominasi reward, collapse bukan soal tuning tapi soal skala.

## Anggaran eksperimen
- Tahap 0: ~2-4 run (gating, wajib lebih dulu)
- Tahap 1: 6 kombinasi x 3 seed = 18 run (+ rerun finalis 5 seed)
- Tahap 2: 18 kombinasi x 3 seed = 54 run (+ rerun pemenang 5 seed)
- Total ~ 76-80 run, TAPI Tahap 2 hanya dijalankan kalau Tahap 0 = feasible.

## Catatan jujur
Ambang kecepatan 0.04 melawan kebutuhan task (butuh ~0.07 untuk capai goal), dan
karena cost proporsional, anggaran 15 hanya memberi ruang ~5 step di kecepatan
puncak. Itu sebabnya Tahap 0 (probe feasibility) ada di depan: kalau return ikut
turun di semua seed setelah fix, itu sinyal tension struktural — longgarkan
cost_limit/ambang lewat bagian "Kalau infeasible", bukan terus menyetel lambda.
