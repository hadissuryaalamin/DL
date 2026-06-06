# Video Report — 5-Minute Cut
### Safe PPO on MountainCar (3 presenters)

**Target:** 5:00. ~3 beats each for A/B/C. Narration is spoken-style and intentionally skips detail.
Slides for this cut live in `video_report_deck.pptx` (narration is in each slide's speaker notes).

**Thesis (everything builds to this):** *Whether a safety constraint can be met is decided by the
base policy's cost, not its reward.*

| # | Time | Presenter | Slide | Beat |
|---|------|-----------|-------|------|
| 1 | 0:00–0:50 | A | 2 | Hook + the problem |
| 2 | 0:50–1:35 | B | 3–4 | Is it feasible? + how Safe PPO works |
| 3 | 1:35–2:35 | C | 5–6 | Stage 1: screen the bases (the cost gap) |
| 4 | 2:35–3:40 | C→A | 7 | Stage 2: the key finding |
| 5 | 3:40–4:20 | A | 8 | The winner + the λ knob |
| 6 | 4:20–5:00 | B + all | 9–10 | Extensions + three takeaways |

---

### 1 — Hook + problem (A, 0:00–0:50)
**ON SCREEN:** MountainCar clip (a run reaching the flag); cost rule caption; three agent cards.
> "To get this car over the hill it has to build speed — that's the whole puzzle of MountainCar. But
> what if speed is exactly what we want to limit? Energy, wear, safety. So: *can the agent still reach
> the goal while keeping its speed under control?* We add a gentle, proportional cost for going too
> fast, give it a budget of fifteen, and build three agents — DQN, PPO, and Safe PPO — on the same
> environment, so any difference is the safety mechanism, not luck."

### 2 — Feasibility + method (B, 0:50–1:35)
**ON SCREEN:** `cost_vs_speed_cap.png`; then a dual-critic + λ-dial sketch.
> "First, a cheap sanity check — is a safe solution even possible? Hand-coded drivers show: yes, but
> barely. Reckless driving costs nearly double the budget; the most cautious driver that still wins
> bottoms out around eleven. Feasible, but thin.
>
> Safe PPO earns that thin margin with two additions: a second critic that predicts *cost*, and one
> self-tuning number, lambda — a volume knob for safety that turns up when we're over budget and
> relaxes when we're safe. Nobody sets it by hand."

### 3 — Stage 1: screen the bases (C, 1:35–2:35)
**ON SCREEN:** Stage 1 table; `fig4_stage1_selection.png`.
> "We tune in stages. Stage one ignores safety and just finds a good base PPO — six settings, three
> seeds each. Three of them solve the task with basically identical reward, around forty-seven. By
> reward alone they look interchangeable. But we also quietly logged each one's *speed cost* — and it
> differs almost two-to-one. One 'winner' is a speed demon at cost twenty-nine; the others cruise at
> fifteen. Remember that gap."

### 4 — Stage 2: the key finding (C → A, 2:35–3:40)
**ON SCREEN:** `fig5_stage2_scatter.png` revealed in two passes (red cluster fails, then blue/green pass).
> **(C):** "Stage two turns on safety: take the top-three bases and sweep the safety knobs — eighteen
> configurations."
>
> **(A):** "And the result is remarkably clean. *Every* configuration built on the high-cost base
> fails the budget, no matter how we tune. You can't drag a speed-loving policy down to safe speeds
> without it giving up the goal. The low-cost bases, meanwhile, sail into the feasible region. So the
> headline is this: *feasibility is decided by the base's cost, not its reward.* Picking by reward
> alone would have handed us the one base that can never be made safe."

### 5 — The winner + λ (A, 3:40–4:20)
**ON SCREEN:** Winner `training.mp4`; `fig2_safe_dual.png` + `fig3_lambda_cost.png`.
> "The winner reaches full reward as fast as the unconstrained baseline, and its cost settles exactly
> on the budget — we paid essentially nothing to become safe. And watch lambda: it spikes as the car
> first speeds, then relaxes once cost is under control. That curve is the method explaining itself —
> one readable number showing how hard safety is pushing at any moment."

### 6 — Extensions + takeaways (B, then all, 4:20–5:00)
**ON SCREEN:** Roadmap bullets; then three takeaway cards.
> **(B):** "For the final report we'd push the tuning further — confirm the winner on five seeds, sweep
> the budget itself to draw a safety-vs-reward *trade-off curve*, and run the full base-by-safety
> ablation. All of it slots into the existing two-stage runner."
>
> **(C):** "MountainCar is simple enough to *see* how a constraint reshapes learning."
> **(B):** "Lambda is an automatic, readable safety dial."
> **(A):** "And the big one — choose your base policy by its cost, not just its reward. Thanks for watching."
