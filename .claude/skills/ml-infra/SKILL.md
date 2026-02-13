---
name: ml-infra
description: This skill helps maintain structure in machine learning projects by providing some guidelines on what tools to use, defining some standards and expected protocols for configuration, logging, checkpointing.
---

# Overall Purpose

This skill lays out a detailed structure for machine learning projects that makes it amenable to automation. This additional structure allows the information to be pulled and processed in a structured way and works hand in hand with the `wandb-pull-logs` skill.

# Configuration Management
- ALL hyperparameters that modify the model architecture, data loading, preprocessing, training, evaluation, diagnostics, logging, etc. MUST be aggregated into a single configuration file.
- Configuration file should contain detailed header high level model design and how they relate to the defined hyperparameters.
- Each hyperparameter should have a clear comment explaining what its purpose is. Include [default: value] in the comment if applicable.
- Maintain a dictionary mapping of all hyperparameters defined in the configuration file to a shortened name that can be used for identification purposes.
- Seeds should be logged as hyperparameters where applicable and should be used liberally to ensure reproducibility at different stages.
- Ensure usage of `Pydantic` for configuration validation and parsing.
- Ensure config loading fails fast on unknown fields or invalid values (no silent fallback defaults).
- Ensure the fully resolved config (after CLI/hydra overrides) is persisted with every run artifact.

# Hyperparameter Scanning
- Ensure usage of `hydra` for hyperparameter scanning.
- Any CLI setup should respect hydra multirun configuration.
- Ensure that when running with multirun, the checkpointed configuration file is updated with appropriate hyperparameters.
- For wandb run name construction we should ensure that the shortened names are used for cleaner identification.
- Ensure that sequential execution is the default mode for normal and multirun execution.
- Ensure that parallelization is available when multirunning focusing on Slurm clusters.
- Ensure that proper progress tracking is available that monitors the overall progress of the multirun.
- Ensure duplicate parameter combinations are detected and skipped when resuming interrupted multiruns.

# Weights and Biases Checkpointing and Recovery
- Ensure experiment logging is setup using wandb.
- Ensure metrics are logged like "train/loss", "val/loss".
- Ensure plots are logged like "plots/loss_curve".
- Ensure you log the wandb run path in the checkpoint as `wandb_run_path`.
- Ensure the configuration file (with updated hyperparameters) is saved in the checkpoint.
- Ensure code `git commit SHA` is logged to the checkpoint.
- Ensure you save periodic and best checkpoints with clear criteria (for example best `val/loss`).
- Ensure you include model state, optimizer state, scheduler state, scaler state (if mixed precision), global step/epoch, and config.
- Ensure you support resume behavior that restores training state exactly and logs whether a run was resumed.
- Ensure wall-clock timing metrics are logged (`train/step_time`, epoch duration, total runtime) for throughput analysis.
- Ensure checkpoint filenames include stable metadata (epoch, step, metric) to avoid accidental overwrites.
- Ensure important evaluation artifacts are uploaded to wandb artifacts with versioned aliases (for example `best`, `latest`).

# CLI
- Define a canonical CLI entrypoint that is separate from training logic.
- Ensure CLI exposes explicit subcommands such as `train`, `eval`, `multirun`, and `resume`.
- Ensure CLI supports a `--dry-run` mode that validates config, paths, and dependencies without launching training.
- Ensure CLI outputs the resolved config and output directory at startup for reproducibility.

# Testing
- Add smoke tests for one forward pass, one train step, and one eval step.
- Add config validation tests to catch missing/invalid hyperparameters before training starts.
- Add checkpoint round-trip tests that save and restore full training state and confirm step/epoch continuity.
- Add deterministic tests that run with fixed seeds and assert stable metrics within tight tolerance.
- Add a tiny integration test on a minimal dataset to verify end-to-end train -> checkpoint -> eval pipeline.

# Logging
- Log failures with enough context (error type, batch/step info, last checkpoint path) to enable quick debugging.
- Use structured logs (JSON or key-value) that always include run id, seed, dataset version, and git SHA.
- Log data loading and preprocessing diagnostics (sample counts, dropped/invalid rows, class distribution).
