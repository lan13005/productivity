# Package Manager

**Always use `uv` for all package management, tool execution, and script execution.**

- Install dependencies: `uv python -m pip install <package>` or `uv sync`
- Run external tools: `uv run <tool>`
- Execute scripts: `uv run <script>`

# Code Style Highlights

- Type hints required on all functions
- `from __future__ import annotations` for modern syntax
- Google-style docstrings
- Rich console for formatted output
- Dataclasses for configuration
- pathlib.Path for file operations

See `reference/style.md` for complete style guide.

# Style Contracts

Enforce ruff rules: `I001, PLC0415, TC002, RUF002, SIM102, SIM105, BLE001, B904, PLW2901, RET505, PTH123, DTZ007`

- Type hints required on all functions
- `from __future__ import annotations` at top
- Dataclass defaults: `field(default_factory=...)` for mutable defaults

# Git Workflow

- Use conventional commits: `type: description`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.
- Atomic commits with clear, descriptive messages
- Include co-authorship when applicable
