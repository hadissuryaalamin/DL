# Video Report — Concept & Script
### Safe PPO on MountainCar: reaching the goal without speeding

**Format:** ~10-minute narrated video, **3 presenters** (A, B, C), screen-recording + slides + the
training-process videos we already generated.
**Goal:** communicate the *key ideas and the one big finding* — not every number. Each presenter
owns ~3 minutes. Timings are guides, not hard cuts.

**Visual assets we already have** (reuse these, don't rebuild):
- MountainCar env render / `videos/dqn_mountaincar.mp4`
- Feasibility probe plot: `notebooks/cost_vs_speed_cap.png`
- Paper figures: `paper/figures/fig1_learning_curves`, `fig4_stage1_selection`, `fig5_stage2_scatter`, `fig2_safe_dual`, `fig3_lambda_cost`
- Per-run training-process videos with hyperparameters overlaid: `results/<config>/seed_*/training.mp4`
- Comparison grids: `videos/stage2_B*_grid.mp4`, per-config seed grids
- Tables from `results/stage1_summary.md`, `results/stage2_summary.md`, paper Table 1/2

**One-sentence thesis the whole video builds toward:**
> *Whether a safety constraint is satisfiable is decided by the base policy's cost, not its reward —
> so we must screen bases by cost, and our tuned Safe PPO then meets the budget for free.*

---

## Segment map

| # | Time | Presenter | Beat |
|---|------|-----------|------|
| 0 | 0:00–0:40 | A | Cold-open hook |
| 1 | 0:40–2:00 | A | The problem & the three agents |
| 2 | 2:00–3:10 | B | "Is it even possible?" — feasibility probe |
| 3 | 3:10–4:20 | B | How Safe PPO works (the λ knob) |
| 4 | 4:20–5:40 | C | Stage 1 — screening the base policies |
| 5 | 5:40–7:20 | C → A | Stage 2 — the safety sweep & the key finding |
| 6 | 7:20–8:20 | A | The winner, and what λ is doing |
| 7 | 8:20–9:30 | B | Extending the hyperparameter research |
| 8 | 9:30–10:00 | A, B, C | Three takeaways + close |

---

## Segment 0 — Cold open (Presenter A, 0:00–0:40)

**ON SCREEN:** Split screen of two `training.mp4` clips playing — a car flooring it up the hill and
reaching the flag, next to a car moving more gently. No labels yet, just motion. Title card fades in:
*"Safe PPO on MountainCar — learning to win without breaking the rules."*

**NARRATION (A):**
> "To get this little car over the hill, it has to build up speed — that's the whole puzzle of
> MountainCar. But here's a twist: what if going fast is the thing we *don't* want? In a real
> vehicle, speed costs energy, wears parts, and can be unsafe. So our question is simple to say and
> surprisingly hard to do: *can the agent still reach the goal while keeping its speed in check?*
> That's what this project is about."

---

## Segment 1 — The problem & the three agents (Presenter A, 0:40–2:00)

**ON SCREEN:**
- A clean MountainCar diagram (valley, flag, car).
- The cost rule appears as a simple caption, not heavy math:
  `cost per step = (|speed| − 0.04) × 100, only when speed > 0.04`, and a budget line "total ≤ 15".
- Three labelled cards slide in: **DQN**, **PPO**, **Safe PPO**.

**NARRATION (A):**
> "We frame this as a *constrained* reinforcement-learning problem. The agent still earns reward for
> reaching the flag — we add a little shaping so the signal isn't hopelessly sparse — but now every
> step where it exceeds a speed threshold racks up a *cost*. The rule is gentle and proportional:
> the faster you go over the line, the more it costs. The agent's job is to reach the goal while
> keeping its total cost under a budget of fifteen.
>
> We build up to this in three steps. First a **DQN** — a classic value-based agent, our sanity
> check that the task is learnable. Then **PPO** — a strong policy-gradient baseline, but it ignores
> safety entirely. And finally **Safe PPO**, which adds the safety machinery. Everything shares the
> same shaped environment, so any difference we see is the safety mechanism, not luck."

---

## Segment 2 — "Is it even possible?" (Presenter B, 2:00–3:10)

**ON SCREEN:** `notebooks/cost_vs_speed_cap.png` (cost vs speed-cap curve with the dotted budget
line). Animate a pointer sweeping from the aggressive side (left) to the thrifty side (right).

**NARRATION (B):**
> "Before training anything expensive, we asked a cheap question: is there *any* way to solve this
> while staying under budget? We wrote a few hand-coded drivers that 'pump' the car but refuse to
> exceed a chosen speed cap, and just measured their cost.
>
> The answer is: *yes, but barely.* A reckless driver that always floors it costs about twenty-nine —
> almost double the budget. The most cautious driver that can still reach the flag bottoms out around
> eleven. So a safe-and-successful solution exists, but the feasible window is thin. That single
> picture set our expectations for everything that follows: we should be able to hit the budget, but
> we shouldn't expect a lot of slack."

---

## Segment 3 — How Safe PPO works (Presenter B, 3:10–4:20)

**ON SCREEN:** Simple block diagram: shared trunk → **actor**, **reward critic**, **cost critic**.
Then a small animation of a dial labelled **λ** turning up and down. Keep the equations off-screen or
as a single faded line; this is the intuition beat.

**NARRATION (B):**
> "Safe PPO takes ordinary PPO and gives it a second pair of eyes. Alongside the usual critic that
> predicts *reward*, we add a second critic that predicts *cost*. Then we introduce one extra number,
> lambda — think of it as a volume knob for safety.
>
> When the agent is over budget, lambda turns up and the policy is pushed to slow down. When the
> agent is safely under budget, lambda relaxes and the agent is free to chase reward. Nobody sets
> lambda by hand — it adjusts itself every update based on how badly the constraint is being
> violated. That self-tuning knob is the heart of the method, and later you'll literally watch it
> move."

---

## Segment 4 — Stage 1: screening the bases (Presenter C, 4:20–5:40)

**ON SCREEN:**
- Stage 1 table (paper Table 1 / `stage1_summary.md`) — highlight the Return column, then the Avg-cost column.
- `fig4_stage1_selection.pdf`.
- Optional: two short `training.mp4` clips — P1 (never solves) vs P6 (solves smoothly), hyperparameters visible in their headers.

**NARRATION (C):**
> "Now the tuning. Instead of one giant search, we do it in stages, changing only two knobs at a
> time. Stage one ignores safety completely and just looks for a *good base PPO*. We sweep six
> settings of learning rate and exploration, three seeds each.
>
> Two settings never learn, one is wildly unstable, and three solve the task perfectly — and here's
> the subtle part. Those three winners have *identical* reward, around forty-seven. If you ranked
> them by reward alone, they'd look interchangeable. But we also quietly recorded each one's *speed
> cost*, even though PPO never optimizes it — and that cost differs almost two-to-one. One of the
> 'tied' winners is a speed demon at cost twenty-nine; the other two cruise at fifteen. Hold onto
> that gap — it's about to decide everything."

---

## Segment 5 — Stage 2 & the key finding (Presenter C → Presenter A, 5:40–7:20)

**ON SCREEN:**
- `fig5_stage2_scatter.pdf` — reveal it in two passes: first the red P4 cluster all stranded far past
  the budget line, then the blue/green points near the line. Circle the three passing points.
- Cut to a `videos/stage2_B*_grid.mp4` comparison grid so the audience *sees* several runs training at once.
- Table 2 for reference.

**NARRATION (C):**
> "Stage two finally turns on safety. We take the three base winners and, on top of each, sweep the
> safety knobs — how fast lambda adapts and where it starts — eighteen configurations in all."

**NARRATION (A) — deliver the punchline:**
> "And the result is almost comically clean. Look where the configurations land. *Every single one*
> built on the high-cost base — the speed demon — fails the budget, no matter how we tune the safety
> knobs. You simply cannot drag a policy that loves going fast down to safe speeds without it giving
> up on the goal. Meanwhile, the configurations built on the *low-cost* bases sail into the feasible
> region.
>
> So the headline of the whole project is this: *whether you can satisfy the constraint is decided by
> the base you start from — specifically its cost, not its reward.* Picking a base by reward alone,
> the obvious thing to do, would have handed us the one base that can never be made safe. That cheap
> passive-cost number from Stage 1 was the difference between success and failure."

---

## Segment 6 — The winner, and watching λ work (Presenter A, 7:20–8:20)

**ON SCREEN:**
- The winner's `training.mp4` (config S6) — car reaching the goal, with the live reward + cost curves
  and the λ value in the overlay.
- `fig2_safe_dual.pdf` and `fig3_lambda_cost.pdf` side by side.

**NARRATION (A):**
> "Here's the winner. It reaches full reward just as fast as the unconstrained baseline — about
> forty-seven — and its cost settles *exactly* on the budget of fifteen. In other words, we paid
> essentially nothing in performance to become safe.
>
> And watch the safety knob. Early on, as the car first starts speeding, lambda shoots up — the agent
> is being told 'ease off.' Then, once the cost is under control, lambda quietly relaxes and holds
> steady. That curve is the method explaining itself: a single, interpretable number that says, at
> every moment, *how hard safety is currently pushing.*"

---

## Segment 7 — Extending the hyperparameter research (Presenter B, 8:20–9:30)

**ON SCREEN:** A roadmap slide — five bullet items appearing one at a time. Optionally a small
mock "Pareto front" sketch (return on y, cost budget on x) to illustrate the cost-limit sweep.

**NARRATION (B):**
> "What we showed is a first, deliberately disciplined pass. For the final report we'd extend the
> hyperparameter study in a few concrete directions — and our scripts are already built to make most
> of these one command.
>
> First, **confirm the winner with more seeds** — five instead of three — because a champion chosen
> from three runs can still be lucky. Second, **widen the safety grid**: our lambda step sizes were
> close together, so we'd open them up and check we haven't missed a better operating point. Third,
> and most interesting for the report, **sweep the budget itself** — twelve, fifteen, twenty,
> twenty-five — and draw the *trade-off curve* between safety and reward. That turns a single answer
> into a Pareto front, which is a far more honest result. Fourth, run the *full* cross of bases and
> safety settings as an ablation, to nail down the base-cost claim beyond three examples. And finally,
> tighten one measurement detail — the cost used to drive lambda versus the cost we report — so the
> 'feasible' line means exactly one thing. Each of these slots straight into the existing two-stage
> runner."

---

## Segment 8 — Takeaways & close (all three, 9:30–10:00)

**ON SCREEN:** Three one-line cards, each lighting up as its presenter speaks, over a quiet loop of
the winning run. End card with the project/paper title and "code + paper available."

**NARRATION:**
- **C:** "MountainCar is simple enough to *see* how a safety constraint reshapes learning."
- **B:** "A Lagrangian multiplier is an automatic, readable safety dial — and you can watch it work."
- **A:** "And the big one: to satisfy a constraint, choose your starting policy by its cost, not just
  its reward. Thanks for watching."

---

# Appendix: Hyperparameter research — extension plan for the final report

This is the written version of Segment 7, with enough specifics to execute and cite. Most items map
directly onto `scripts/run_stage1.py` / `scripts/run_stage2.py`.

**1. Five-seed confirmation of finalists.**
Re-run the Stage-1 top-3 bases and the Stage-2 passing configs (S4, S6, S10) with 5 seeds. Standard
deviations from 3 samples are unreliable; the selection script already flags this. Report the winner's
mean ± std on 5 seeds before any final claim.
*Command:* `python -m scripts.run_stage2 --combos S4 S6 S10 --seeds 0 1 2 3 4`.

**2. Widen / re-center the safety grid.**
Our `lam_lr ∈ {0.02, 0.03, 0.05}` spans only 2.5×. If the λ trajectories look sluggish or jittery,
switch to `{0.01, 0.03, 0.1}` rather than adding rows. If `log_lambda_init` turns out low-impact
(odd vs. even S-rows look identical), fix it at the better value and spend that axis on something else.

**3. Budget sweep → Pareto front (highest-value addition).**
Sweep `cost_limit ∈ {12, 15, 20, 25}` on the winning base and plot final return vs. achieved cost.
This converts a single point into a *return–safety trade-off curve* and directly tests the
feasibility-probe prediction that the floor is ~11. If no point is both safe and solving, the curve
itself is the honest result. *Command:* repeat `run_stage2` with `--cost-limit <d>` per value.

**4. Full base × safety cross (ablation for the key claim).**
Run all six bases in Stage 2 (not just the top-3) so the "base cost predicts feasibility" claim rests
on 36 configurations rather than 18. This is the clean ablation a reviewer will want.
*Command:* `python -m scripts.run_stage2 --bases P1 P2 P3 P4 P5 P6`. (Note the compute: ~2× Stage 2.)

**5. Reconcile the cost metric, then re-tune.**
Currently λ is updated against the *discounted* cost-return while feasibility is checked against the
*undiscounted* episode cost. Align them (recommend undiscounted for both), then re-run the winner's
neighborhood — the "pass / fail" boundary should sharpen.

**6. Beyond grid search (stretch).**
Replace the staged grid with a small random or Bayesian search over the joint space (lr, β, α_λ, ℓ₀)
to check the grid didn't miss a better region; and prototype a **PID-Lagrangian** λ-controller to
widen the narrow stable band we observed (S8's collapse shows the current pure-gradient controller is
easy to over-drive).

**Reporting checklist for the final paper:**
- Per-config table with 5-seed mean ± std (extend Table 2).
- The Pareto front figure (item 3) as a new headline figure.
- The full-cross ablation (item 4) supporting the base-cost claim.
- A short "search budget" note: how many runs, total wall-clock, and what was *not* searched.
