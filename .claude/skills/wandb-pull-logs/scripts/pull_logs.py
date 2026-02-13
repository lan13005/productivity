#!/usr/bin/env python3
"""Pull W&B run metrics and hyperparameters (agent-optimized).

Standalone utility that fetches from checkpoints (extracting wandb_run_path)
or direct wandb run paths. Caches wandb data in checkpoints for fast subsequent access.
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import datetime
from typing import Any, List, Mapping, NoReturn, Optional

import numpy as np
import pandas as pd
import torch


FILTER_EXPR_PATTERN = re.compile(
    r"^(?P<column>[a-zA-Z0-9_./-]+)\s*(?P<operator>>=|<=|==|!=|>|<)\s*(?P<value>[\d.eE+-]+)$"
)


def _die(message: str) -> NoReturn:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def _is_numeric_summary_val(val: Any) -> bool:
    """True if value is a displayable numeric (int/float, not NaN)."""
    if val is None:
        return False
    if isinstance(val, bool):
        return False
    if isinstance(val, (int, float)) and math.isnan(float(val)):
        return False
    return isinstance(val, (int, float))


def _numeric_summary(summary: Mapping[str, Any]) -> dict:
    return {k: v for k, v in summary.items() if _is_numeric_summary_val(v)}


def _flatten_config(config: Mapping[str, Any], prefix: str = "") -> dict:
    """Flatten nested config dict to dot-notation keys."""
    flat = {}
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(_flatten_config(value, full_key))
        else:
            flat[full_key] = value
    return flat


def _load_checkpoint(path: str) -> dict:
    try:
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    except Exception as exc:
        _die(f"Failed to load checkpoint '{path}': {exc}")
    if not isinstance(checkpoint, dict):
        _die(f"Checkpoint is not a dictionary: {path}")
    return checkpoint


def _restore_history_from_cache(cache: dict) -> pd.DataFrame:
    history = cache.get("history")
    if history is None:
        return pd.DataFrame()
    if isinstance(history, pd.DataFrame):
        return history
    if isinstance(history, list):
        df = pd.DataFrame(history)
    elif isinstance(history, dict):
        if {"index", "columns", "data"}.issubset(history.keys()):
            df = pd.DataFrame(**history)
        else:
            df = pd.DataFrame(history)
    else:
        return pd.DataFrame()
    if "step" in df.columns:
        df = df.set_index("step")
    if df.index.name != "step":
        df.index.name = "step"
    return df


def _build_history_for_cache(history_df: pd.DataFrame) -> dict:
    frame = history_df.reset_index()
    if "step" not in frame.columns:
        frame = frame.rename(columns={frame.columns[0]: "step"})
    return frame.to_dict(orient="split")


def _clean_history(history_df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = history_df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return pd.DataFrame()
    cleaned = history_df[numeric_cols].dropna(how="all")
    if "_step" in cleaned.columns:
        cleaned = cleaned.set_index("_step")
    elif "step" in cleaned.columns:
        cleaned = cleaned.set_index("step")
    cleaned.index.name = "step"
    return cleaned


def _has_history_data(history: Any) -> bool:
    return history is not None and isinstance(history, pd.DataFrame) and not history.empty


def _get_wandb_data(
    run_path: str, checkpoint_path: Optional[str] = None, refresh: bool = False
) -> dict:
    """Fetch wandb data, using cache if available.

    Returns dict with:
      - fetched_at: ISO timestamp
      - config: flattened hyperparameters
      - summary: final metric values
      - history: pd.DataFrame with step as index, metrics as columns
      - name: run name
    """
    checkpoint = _load_checkpoint(checkpoint_path) if checkpoint_path else None

    # Prefer checkpoint cache unless a refresh is requested.
    if checkpoint_path and not refresh:
        cache = checkpoint.get("wandb_cache")
        if isinstance(cache, dict) and cache:
            cache = cache.copy()
            cache["history"] = _restore_history_from_cache(cache)
            return cache

    try:
        import wandb
    except ImportError:
        _die("wandb is not installed. Run: pip install wandb")

    api = wandb.Api()
    try:
        run = api.run(run_path)
    except wandb.errors.CommError as e:
        _die(f"Could not fetch run '{run_path}': {e}")

    history_clean = _clean_history(run.history())

    cache = {
        "fetched_at": datetime.now().isoformat(),
        "name": run.name,
        "config": _flatten_config(dict(run.config)),
        "summary": _numeric_summary(
            {k: v for k, v in run.summary.items() if not k.startswith("_")}
        ),
        "history": history_clean,
    }

    if checkpoint is not None:
        cache_for_save = cache.copy()
        cache_for_save["history"] = _build_history_for_cache(history_clean)
        checkpoint["wandb_cache"] = cache_for_save
        torch.save(checkpoint, checkpoint_path)

    return cache


def _select_metrics(history_df, pattern: str):
    """Filter DataFrame columns by exact name match."""
    if history_df is None or history_df.empty:
        return history_df

    wanted = {p.strip() for p in pattern.split("|") if p.strip()}
    matching_cols = [c for c in history_df.columns if c in wanted]
    if not matching_cols:
        missing = wanted - set(history_df.columns)
        print(
            f"Warning: No metrics match. Requested: {sorted(wanted)}. "
            f"Missing: {sorted(missing)}",
            file=sys.stderr,
        )
        return pd.DataFrame()
    return history_df[matching_cols]


def _filter_rows(history_df, expr: str):
    """Filter DataFrame rows using inequality expression."""
    if history_df is None or history_df.empty:
        return history_df

    match = FILTER_EXPR_PATTERN.match(expr.strip())
    if not match:
        _die(f"Invalid filter expression: {expr}")

    col = match.group("column")
    op = match.group("operator")
    val = float(match.group("value"))

    if col == "step":
        series = history_df.index.to_series()
    elif col not in history_df.columns:
        _die(f"Column not found: {col}")
    else:
        series = history_df[col]

    ops = {
        ">": lambda x: x > val,
        "<": lambda x: x < val,
        ">=": lambda x: x >= val,
        "<=": lambda x: x <= val,
        "==": lambda x: x == val,
        "!=": lambda x: x != val,
    }

    mask = ops[op](series).fillna(False)
    return history_df.loc[mask]


def _wrap_column_names(expr: str, columns: list) -> str:
    """Wrap column names containing special chars in backticks for pandas eval."""
    cols_to_wrap = sorted(
        [c for c in columns if not c.isidentifier()], key=len, reverse=True
    )

    result = expr
    for col in cols_to_wrap:
        pattern = re.escape(col)
        result = re.sub(rf"(?<![`\w]){pattern}(?![`\w])", f"`{col}`", result)
    return result


def _apply_eval(history_df, expr: str):
    """Compute a derived column using pandas eval."""
    if history_df is None or history_df.empty:
        return history_df

    if "=" not in expr:
        _die(f"Eval expression must be 'name=expression': {expr}")

    name, formula = expr.split("=", 1)
    name = name.strip()
    formula = formula.strip()
    if not name:
        _die(f"Eval expression has empty output column: {expr}")

    wrapped_formula = _wrap_column_names(formula, history_df.columns.tolist())

    try:
        history_df[name] = history_df.eval(wrapped_formula)
    except Exception as e:
        _die(f"Error evaluating '{expr}': {e}")

    return history_df


def _filter_nan_rows(history_df, hide_any_nan: bool = True):
    """Filter out rows containing NaN.

    If hide_any_nan is True (default): drop rows where any value is NaN.
    If False: drop only rows where all values are NaN.
    """
    if history_df is None or history_df.empty:
        return history_df
    how = "any" if hide_any_nan else "all"
    return history_df.dropna(how=how)


def _format_scalar(value: Any, precision: int = 4) -> str:
    if pd.isna(value):
        return "nan"
    if isinstance(value, float):
        return f"{value:.{precision}g}"
    return str(value)


def _print_history_table(history: pd.DataFrame, file) -> None:
    cols = list(history.columns)
    print(f"# step | {' | '.join(cols)}", file=file)
    for idx, row in history.iterrows():
        values = [_format_scalar(row[c]) for c in cols]
        print(f"{idx} | {' | '.join(values)}", file=file)


def _print_key_value_block(
    data: Mapping[str, Any], file, empty_message: str, format_floats: bool = False
) -> None:
    if not data:
        print(empty_message, file=file)
        return
    max_key_len = max(len(k) for k in data.keys())
    for key in sorted(data.keys()):
        value = data[key]
        if format_floats and isinstance(value, float):
            print(f"{key:<{max_key_len}} = {value:.6g}", file=file)
        else:
            print(f"{key:<{max_key_len}} = {value}", file=file)


def _output_json_v2(runs_data: List[dict], file) -> None:
    """Output runs data as JSON (v2 format)."""
    output = {"runs": []}
    for data in runs_data:
        run_out = {
            "run_path": data["run_path"],
            "name": data.get("name", ""),
            "fetched_at": data.get("fetched_at", ""),
            "config": data.get("config", {}),
            "summary": _numeric_summary(data.get("summary", {})),
        }
        history = data.get("history")
        if _has_history_data(history):
            run_out["history"] = history.reset_index().to_dict(orient="records")
        output["runs"].append(run_out)

    json.dump(output, file, indent=2, default=str)
    file.write("\n")


def _output_csv_v2(runs_data: List[dict], file) -> None:
    """Output runs data as CSV (history only for single run)."""
    if len(runs_data) == 1:
        history = runs_data[0].get("history")
        if _has_history_data(history):
            history.reset_index().to_csv(file, index=False)
        else:
            print("# No history data", file=file)
    else:
        rows = []
        for data in runs_data:
            row = {
                "run_path": data["run_path"],
                "name": data.get("name", ""),
            }
            row.update(_numeric_summary(data.get("summary", {})))
            rows.append(row)

        if rows:
            all_cols = set()
            for row in rows:
                all_cols.update(row.keys())
            cols = ["run_path", "name"] + sorted(
                c for c in all_cols if c not in ("run_path", "name")
            )

            writer = csv.DictWriter(file, fieldnames=cols)
            writer.writeheader()
            writer.writerows(rows)


def _output_single_run_agent(
    data: dict,
    file,
    show_schema: bool,
    show_stats: bool,
    human_mode: bool,
) -> None:
    """Output a single run in agent format."""
    run_path = data.get("run_path", "unknown")
    name = data.get("name", "unknown")
    fetched_at = data.get("fetched_at", "")
    config = data.get("config", {})
    summary = _numeric_summary(data.get("summary", {}))
    history = data.get("history")

    print(f"# Run: {name} ({run_path})", file=file)
    if fetched_at:
        print(f"# Fetched at: {fetched_at}", file=file)
    print("", file=file)

    if show_schema:
        print("[SCHEMA]", file=file)
        print(f"# Metric schema for run: {name} ({run_path})", file=file)
        print("#", file=file)
        if _has_history_data(history):
            print(f"# METRICS ({len(history.columns)} total):", file=file)
            print("# Name                          | Type  | Range", file=file)
            for col in sorted(history.columns):
                dtype = (
                    "float"
                    if pd.api.types.is_float_dtype(history[col].dtype)
                    else str(history[col].dtype)
                )
                col_data = history[col].dropna()
                if not col_data.empty:
                    min_val = col_data.min()
                    max_val = col_data.max()
                    print(f"{col:<32} | {dtype:<5} | [{min_val:.3g}, {max_val:.3g}]", file=file)
                else:
                    print(f"{col:<32} | {dtype:<5} | [no data]", file=file)
        else:
            print("# (no history data)", file=file)
        print("", file=file)
        return

    if show_stats:
        print("[STATS]", file=file)
        if _has_history_data(history):
            stats_data = []
            for col in sorted(history.columns):
                col_data = history[col].dropna()
                if not col_data.empty:
                    row = {
                        "metric": col,
                        "min": col_data.min(),
                        "p10": col_data.quantile(0.1),
                        "p25": col_data.quantile(0.25),
                        "p50": col_data.quantile(0.5),
                        "p75": col_data.quantile(0.75),
                        "p90": col_data.quantile(0.9),
                        "max": col_data.max(),
                    }
                    stats_data.append(row)

            if stats_data:
                max_name_len = max(len(r["metric"]) for r in stats_data)
                header = (
                    f"{'metric':<{max_name_len}} | {'min':>8} | {'p10':>8} | {'p25':>8} | "
                    f"{'p50':>8} | {'p75':>8} | {'p90':>8} | {'max':>8}"
                )
                print(header, file=file)
                print("-" * len(header), file=file)
                for row in stats_data:
                    print(
                        f"{row['metric']:<{max_name_len}} | {row['min']:>8.4g} | "
                        f"{row['p10']:>8.4g} | {row['p25']:>8.4g} | {row['p50']:>8.4g} | "
                        f"{row['p75']:>8.4g} | {row['p90']:>8.4g} | {row['max']:>8.4g}",
                        file=file,
                    )
        else:
            print("# (no history data)", file=file)
        print("", file=file)
        return

    print("[CONFIG]", file=file)
    _print_key_value_block(config, file, "# (no config)")
    print("", file=file)

    print("[SUMMARY]", file=file)
    _print_key_value_block(summary, file, "# (no summary metrics)", format_floats=True)
    print("", file=file)

    if not human_mode:
        print("[HISTORY]", file=file)
        if _has_history_data(history):
            _print_history_table(history, file)
        else:
            print("# (no history data)", file=file)
        print("", file=file)


def _output_comparison_agent(
    runs_data: List[dict],
    file,
    show_schema: bool,
    show_stats: bool,
    human_mode: bool,
    show_all: bool = False,
) -> None:
    """Output multi-run comparison in agent format."""
    if show_schema or show_stats:
        for data in runs_data:
            _output_single_run_agent(data, file, show_schema, show_stats, human_mode=True)
        return

    print("[COMPARISON]", file=file)
    print(f"# Comparing {len(runs_data)} runs", file=file)
    print("", file=file)

    run_names = [d.get("name", f"run{i}") for i, d in enumerate(runs_data)]

    print("[CONFIG_DIFF]", file=file)
    print("# Parameters that differ between runs:", file=file)

    all_config_keys = set()
    for d in runs_data:
        all_config_keys.update(d.get("config", {}).keys())

    diff_keys = []
    for key in sorted(all_config_keys):
        values = [d.get("config", {}).get(key) for d in runs_data]
        if len(set(str(v) for v in values)) > 1:
            diff_keys.append(key)

    if diff_keys:
        name_widths = [max(len(name), 12) for name in run_names]
        key_width = max(len(k) for k in diff_keys)

        header = f"{'parameter':<{key_width}}"
        for name, width in zip(run_names, name_widths):
            header += f" | {name:<{width}}"
        print(header, file=file)
        print("-" * len(header), file=file)

        for key in diff_keys:
            row = f"{key:<{key_width}}"
            for d, width in zip(runs_data, name_widths):
                val = d.get("config", {}).get(key, "")
                val_str = str(val)[:width]
                row += f" | {val_str:<{width}}"
            print(row, file=file)
    else:
        print("# (all configs identical)", file=file)
    print("", file=file)

    print("[SUMMARY_COMPARISON]", file=file)

    run_summaries = [_numeric_summary(run.get("summary", {})) for run in runs_data]
    all_summary_keys = {key for summary in run_summaries for key in summary.keys()}

    if all_summary_keys and len(runs_data) >= 2:
        filtered_keys = []
        for key in sorted(all_summary_keys):
            values = [summary.get(key) for summary in run_summaries]
            if not show_all:
                all_present = all(v is not None for v in values)
                if not all_present:
                    continue

            filtered_keys.append(key)

        if filtered_keys:
            name_widths = [max(len(name), 12) for name in run_names]
            key_width = max(len(k) for k in filtered_keys)

            header = f"{'metric':<{key_width}}"
            for name, width in zip(run_names, name_widths):
                header += f" | {name:<{width}}"
            if len(runs_data) == 2:
                header += " | delta"
            print(header, file=file)
            print("-" * len(header), file=file)

            for key in filtered_keys:
                row = f"{key:<{key_width}}"
                values = []
                for summary, width in zip(run_summaries, name_widths):
                    val = summary.get(key, "")
                    val_str = _format_scalar(val)[:width]
                    row += f" | {val_str:<{width}}"
                    values.append(val)

                if len(runs_data) == 2:
                    v1, v2 = values[0], values[1]
                    if _is_numeric_summary_val(v1) and _is_numeric_summary_val(v2):
                        delta = v2 - v1
                        is_loss = any(
                            x in key.lower() for x in ["loss", "error", "mse", "mae"]
                        )
                        if delta < 0:
                            better = "(better)" if is_loss else "(worse)"
                        elif delta > 0:
                            better = "(worse)" if is_loss else "(better)"
                        else:
                            better = ""
                        row += f" | {delta:+.4g} {better}"
                    else:
                        row += " | -"
                print(row, file=file)
        else:
            print(
                "# (no comparable summary metrics - use --show-all to see all)",
                file=file,
            )
    else:
        print("# (no summary metrics)", file=file)
    print("", file=file)

    # History comparison (step-by-step timeseries)
    if not human_mode:
        print("[HISTORY_COMPARISON]", file=file)
        histories = []
        for i, d in enumerate(runs_data):
            h = d.get("history")
            if _has_history_data(h):
                h = h.copy()
                # Use run index to avoid column clashes when run names duplicate
                h.columns = [f"{c} (run{i})" for c in h.columns]
                histories.append((i, h))

        if not histories:
            print("# (no history data)", file=file)
        else:
            # Outer join on step
            merged = histories[0][1]
            for _, h in histories[1:]:
                merged = merged.join(h, how="outer")
            merged = merged.sort_index()

            if not show_all:
                merged = merged.dropna(how="any")

            cols = list(merged.columns)
            if cols:
                _print_history_table(merged, file)
            else:
                print("# (no history columns)", file=file)
        print("", file=file)


def _output_agent_format(
    runs_data: List[dict],
    file,
    show_schema: bool = False,
    show_stats: bool = False,
    human_mode: bool = False,
    show_all: bool = False,
) -> None:
    """Output in agent-optimized structured text format."""
    print("# PULL-LOGS OUTPUT", file=file)
    print("# ================", file=file)
    print("# W&B run data optimized for agent consumption.", file=file)
    print("#", file=file)
    print("# WORKFLOW FOR AGENTS:", file=file)
    print("# 1. Get schema first:   pull-logs -c <ckpt> --schema", file=file)
    print("# 2. Get statistics:     pull-logs -c <ckpt> --stats", file=file)
    print("# 3. Filter by metric:   pull-logs -c <ckpt> --select \"val/loss|train/loss\"", file=file)
    print("# 4. Filter by value:    pull-logs -c <ckpt> --where \"epoch > 5\"", file=file)
    print("# 5. Compute columns:    pull-logs -c <ckpt> --eval \"gap=train/loss - val/loss\"", file=file)
    print("# 6. Compare runs:       pull-logs -c <ckpt1> -c <ckpt2>", file=file)
    print("# 7. Human-readable:     pull-logs -c <ckpt> -H", file=file)
    print("# 8. Show all rows:      pull-logs -c <ckpt> --show-all", file=file)
    print("#", file=file)

    if len(runs_data) == 1:
        _output_single_run_agent(runs_data[0], file, show_schema, show_stats, human_mode)
    else:
        _output_comparison_agent(
            runs_data, file, show_schema, show_stats, human_mode, show_all
        )


def main() -> None:
    """Pull W&B run metrics and hyperparameters (agent-optimized)."""
    parser = argparse.ArgumentParser(
        prog="pull-logs",
        description="Pull W&B run metrics and hyperparameters (agent-optimized output).",
    )
    parser.add_argument(
        "--checkpoint",
        "-c",
        action="append",
        dest="checkpoints",
        metavar="PATH",
        help="Path to checkpoint file (can be specified multiple times)",
    )
    parser.add_argument(
        "--run",
        "-r",
        action="append",
        dest="runs",
        metavar="PATH",
        help="W&B run path (entity/project/run_id) (can be specified multiple times)",
    )
    parser.add_argument(
        "-H",
        "--human",
        action="store_true",
        help="Human-readable mode (hide history for quick overview)",
    )
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Show metric schema (names, types, value ranges)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show summary statistics for each metric (percentiles)",
    )
    parser.add_argument(
        "--select",
        "-s",
        metavar="PATTERN",
        help="Pipe-separated metric names to select (e.g. 'val/loss|train/loss')",
    )
    parser.add_argument(
        "--where",
        "-w",
        metavar="EXPR",
        help="Row filter expression (e.g. 'epoch > 5', 'step >= 100')",
    )
    parser.add_argument(
        "--eval",
        "-e",
        action="append",
        dest="evals",
        metavar="EXPR",
        help="Compute derived column: 'name=expression' (e.g. 'gap=train/loss - val/loss')",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["agent", "json", "csv"],
        default="agent",
        help="Output format (default: agent)",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh from W&B (ignore cache)",
    )
    parser.add_argument(
        "--show-all",
        "-a",
        action="store_true",
        help="Show all rows including NaN (default: hide rows with any NaN)",
    )

    parsed = parser.parse_args()

    run_infos = []

    if parsed.checkpoints:
        for ckpt_path in parsed.checkpoints:
            if not os.path.exists(ckpt_path):
                _die(f"Checkpoint not found: {ckpt_path}")
            checkpoint = _load_checkpoint(ckpt_path)
            wandb_run_path = checkpoint.get("wandb_run_path")
            if not wandb_run_path:
                _die(f"Checkpoint has no wandb_run_path: {ckpt_path}")
            run_infos.append((wandb_run_path, ckpt_path))

    if parsed.runs:
        for run_path in parsed.runs:
            run_infos.append((run_path, None))

    if not run_infos:
        parser.print_help()
        _die("Must specify at least one --checkpoint or --run")

    missing = object()
    unique_by_run = {}
    for run_path, ckpt_path in run_infos:
        existing = unique_by_run.get(run_path, missing)
        if existing is missing or (existing is None and ckpt_path is not None):
            unique_by_run[run_path] = ckpt_path
    run_infos = [(run_path, ckpt_path) for run_path, ckpt_path in unique_by_run.items()]

    runs_data = []
    for run_path, ckpt_path in run_infos:
        data = _get_wandb_data(run_path, ckpt_path, refresh=parsed.refresh)
        data["run_path"] = run_path
        data["checkpoint_path"] = ckpt_path
        runs_data.append(data)

    if parsed.where:
        for data in runs_data:
            data["history"] = _filter_rows(data["history"], parsed.where)

    if parsed.select:
        for data in runs_data:
            data["history"] = _select_metrics(data["history"], parsed.select)

    if parsed.evals:
        for data in runs_data:
            for eval_expr in parsed.evals:
                data["history"] = _apply_eval(data["history"], eval_expr)

    # Filter NaN rows: for single run, filter here; for multi-run, comparison does it after merge
    if not parsed.show_all and len(runs_data) == 1:
        for data in runs_data:
            data["history"] = _filter_nan_rows(data["history"], hide_any_nan=True)

    output_file = sys.stdout
    if parsed.output:
        try:
            output_file = open(parsed.output, "w")
        except OSError as exc:
            _die(f"Could not open output file '{parsed.output}': {exc}")

    try:
        if parsed.format == "json":
            _output_json_v2(runs_data, output_file)
        elif parsed.format == "csv":
            _output_csv_v2(runs_data, output_file)
        else:
            _output_agent_format(
                runs_data,
                output_file,
                show_schema=parsed.schema,
                show_stats=parsed.stats,
                human_mode=parsed.human,
                show_all=parsed.show_all,
            )
    finally:
        if parsed.output:
            output_file.close()
            print(f"Output written to {parsed.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
