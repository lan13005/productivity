---
name: wandb-pull-logs
description: Fetches W&B run metrics and hyperparameters for agent analysis. Use when analyzing or comparing wandb experiments, inspecting training runs, comparing checkpoints, or when the user asks about experiment results, metrics, or run comparisons.
---

# wandb-pull-logs

Context-providing skill for analyzing and comparing wandb experiments. Run the bundled pull-logs script to fetch run data, then use the structured output as context for analysis. Does not modify files.

## When to Use

- User asks about wandb experiments, training runs, or metrics
- Comparing runs or checkpoints
- Inspecting experiment results, hyperparameters, or learning curves
- Need schema, statistics, or filtered views of run data

## How to Run

From project root (herddit or any project with checkpoints):

```bash
cd .cursor/skills/wandb-pull-logs && uv run python scripts/pull_logs.py -c path/to/checkpoint.pt
```

Or with `--project` from repo root:

```bash
uv run --project .cursor/skills/wandb-pull-logs python .cursor/skills/wandb-pull-logs/scripts/pull_logs.py -c checkpoints/best.pt
```

**Inputs:**
- `-c` / `--checkpoint`: Path to checkpoint file (herddit checkpoints with `wandb_run_path`). Can repeat for comparison.
- `-r` / `--run`: Direct W&B run path (`entity/project/run_id`). Can repeat.

## Workflow for Agents

1. **Schema first**: `--schema` — see metric names, types, value ranges
2. **Statistics**: `--stats` — percentiles (p10/25/50/75/90), min, max
3. **Filter metrics**: `--select "loss|epoch"` — regex to select columns
4. **Filter rows**: `--where "epoch > 5"` — inequality filter
5. **Derived columns**: `--eval "gap=train/loss - val/loss"` — pandas expressions
6. **Compare runs**: `-c ckpt1.pt -c ckpt2.pt` — side-by-side config diff and metric deltas
7. **Human mode**: `-H` — compact output without full history
8. **Show all rows**: `--show-all` — include NaN rows (hidden by default)

## Output Format

Structured sections for context:

| Section | Content |
|---------|---------|
| `[CONFIG]` | Flattened hyperparameters |
| `[SUMMARY]` | Final metric values |
| `[HISTORY]` | Step-indexed metrics (hidden in `-H` mode) |
| `[SCHEMA]` | Metric names, types, ranges (with `--schema`) |
| `[STATS]` | Percentiles (with `--stats`) |
| `[COMPARISON]` | Multi-run comparison |
| `[CONFIG_DIFF]` | Parameters that differ between runs |
| `[SUMMARY_COMPARISON]` | Summary metrics with deltas |

## Example Commands

```bash
# Basic: config, summary, history
uv run python scripts/pull_logs.py -c checkpoints/best.pt

# Quick overview (no history)
uv run python scripts/pull_logs.py -c checkpoints/best.pt -H

# Schema and stats
uv run python scripts/pull_logs.py -c checkpoints/best.pt --schema
uv run python scripts/pull_logs.py -c checkpoints/best.pt --stats

# Filter and derive
uv run python scripts/pull_logs.py -c checkpoints/best.pt --select "loss|epoch" --where "epoch > 5"
uv run python scripts/pull_logs.py -c checkpoints/best.pt --eval "gap=train/loss - val/loss"

# Compare two runs
uv run python scripts/pull_logs.py -c ckpt1.pt -c ckpt2.pt

# Force refresh from wandb
uv run python scripts/pull_logs.py -c checkpoints/best.pt --refresh
```

Run from `.cursor/skills/wandb-pull-logs/`; adjust checkpoint paths (e.g. `../../checkpoints/best.pt`) when needed.
