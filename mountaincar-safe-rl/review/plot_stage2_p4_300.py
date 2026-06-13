"""Plot and summarize the P4 Stage-2 150-vs-300 epoch extension.

Run from the repo root:
    .venv/bin/python review/plot_stage2_p4_300.py

Outputs:
    review/stage2_p4_150_vs_300.png
    review/stage2_p4_300_summary.md
"""
from __future__ import annotations

import json
import statistics as stats
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "review"
RESULTS_DIR = ROOT / "results"
LAST_K = 10
PAIRS = [
    ("S13", "S19", 0.02, -1.0),
    ("S14", "S20", 0.02, 0.0),
    ("S15", "S21", 0.03, -1.0),
    ("S16", "S22", 0.03, 0.0),
    ("S17", "S23", 0.05, -1.0),
    ("S18", "S24", 0.05, 0.0),
]


def last_k(values: list[float]) -> float:
    return float(np.mean(values[-LAST_K:])) if values else float("nan")


def read_config(sid: str) -> dict:
    rows = []
    for seed in [0, 1, 2]:
        path = RESULTS_DIR / f"safe_{sid}" / f"seed_{seed}" / "metrics.json"
        m = json.load(open(path))
        rows.append({
            "seed": seed,
            "ret": last_k(m["epoch_returns"]),
            "cost": last_k(m["epoch_costs"]),
            "lam": last_k(m["epoch_lambdas"]),
            "solved": last_k(m["epoch_solved_rates"]),
            "epochs": len(m["epoch_returns"]),
        })
    return {
        "sid": sid,
        "epochs": rows[0]["epochs"],
        "ret_mean": stats.mean(r["ret"] for r in rows),
        "ret_std": stats.pstdev(r["ret"] for r in rows),
        "cost_mean": stats.mean(r["cost"] for r in rows),
        "cost_std": stats.pstdev(r["cost"] for r in rows),
        "lam_mean": stats.mean(r["lam"] for r in rows),
        "solved_mean": stats.mean(r["solved"] for r in rows),
        "seed_costs": [r["cost"] for r in rows],
        "seed_returns": [r["ret"] for r in rows],
    }


def main() -> None:
    rows = []
    for old, new, lam_lr, log_lam0 in PAIRS:
        old_stats = read_config(old)
        new_stats = read_config(new)
        rows.append({
            "old": old_stats,
            "new": new_stats,
            "lam_lr": lam_lr,
            "log_lam0": log_lam0,
        })

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    colors = plt.cm.tab10(np.linspace(0, 1, len(rows)))

    for idx, (row, color) in enumerate(zip(rows, colors)):
        old = row["old"]
        new = row["new"]
        label = f"{old['sid']}->{new['sid']}  lr={row['lam_lr']}, loglam0={row['log_lam0']:g}"

        axes[0].errorbar(
            [idx - 0.16, idx + 0.16],
            [old["cost_mean"], new["cost_mean"]],
            yerr=[old["cost_std"], new["cost_std"]],
            fmt="o-",
            color=color,
            capsize=3,
            label=label,
        )
        axes[1].arrow(
            old["cost_mean"],
            old["ret_mean"],
            new["cost_mean"] - old["cost_mean"],
            new["ret_mean"] - old["ret_mean"],
            length_includes_head=True,
            head_width=0.45,
            head_length=0.9,
            color=color,
            alpha=0.85,
        )
        axes[1].scatter(old["cost_mean"], old["ret_mean"], marker="x", color=color, s=70)
        axes[1].scatter(new["cost_mean"], new["ret_mean"], marker="o", color=color, s=60)
        axes[1].text(new["cost_mean"] + 0.25, new["ret_mean"], new["sid"], fontsize=8)

    axes[0].axhline(15, color="black", linestyle="--", linewidth=1, label="budget d=15")
    axes[0].set_xticks(range(len(rows)))
    axes[0].set_xticklabels([f"{r['old']['sid']}->{r['new']['sid']}" for r in rows], rotation=35)
    axes[0].set_ylabel("Episode cost (last-10 mean)")
    axes[0].set_title("P4 Stage-2 cost: 150 epochs vs 300 epochs")
    axes[0].grid(alpha=0.25, axis="y")

    axes[1].axvline(15, color="black", linestyle="--", linewidth=1)
    axes[1].set_xlabel("Episode cost (lower is safer)")
    axes[1].set_ylabel("Return (higher is better)")
    axes[1].set_title("Cost-return movement after extending horizon")
    axes[1].grid(alpha=0.25)

    fig.suptitle("Original Safe PPO only: extending P4 Stage-2 configs from 150 to 300 epochs")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=[0, 0.16, 1, 0.93])

    out_png = REVIEW_DIR / "stage2_p4_150_vs_300.png"
    fig.savefig(out_png, dpi=160)

    pass_count = sum(r["new"]["cost_mean"] <= 15 for r in rows)
    lines = [
        "# Stage 2 P4 300-epoch extension",
        "",
        "This repeats the original P4 Stage-2 block (S13-S18) with the original Safe PPO",
        "implementation and only one intended change: `epochs: 150 -> 300`. The new IDs",
        "S19-S24 map one-to-one onto S13-S18.",
        "",
        f"Summary: {pass_count}/6 extended P4 configs meet the cost budget by mean cost;",
        "all six solve at full return. S22 is the only mean-cost miss (15.6) and is driven",
        "by one high-cost seed.",
        "",
        f"![P4 150 vs 300 comparison]({out_png.name})",
        "",
        "| 150ep | 300ep | lam_lr | log_lam0 | 150 cost | 300 cost | 150 return | 300 return | 300 solved | pass |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        old = row["old"]
        new = row["new"]
        passed = "yes" if new["cost_mean"] <= 15 else "no"
        lines.append(
            f"| {old['sid']} | {new['sid']} | {row['lam_lr']:.2f} | {row['log_lam0']:.0f} "
            f"| {old['cost_mean']:.1f} +/- {old['cost_std']:.1f} "
            f"| {new['cost_mean']:.1f} +/- {new['cost_std']:.1f} "
            f"| {old['ret_mean']:.1f} +/- {old['ret_std']:.1f} "
            f"| {new['ret_mean']:.1f} +/- {new['ret_std']:.1f} "
            f"| {new['solved_mean']:.2f} | {passed} |"
        )

    lines += [
        "",
        "Seed-level note: S22 has seed costs "
        + ", ".join(f"{v:.1f}" for v in read_config("S22")["seed_costs"])
        + "; the third seed is the reason its mean remains slightly above 15.",
    ]
    out_md = REVIEW_DIR / "stage2_p4_300_summary.md"
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_png}")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
