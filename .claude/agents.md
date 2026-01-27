# Claude Code Reference Guide

Quick reference for development workflows and source code organization.

## Reference Documentation

| Reference Topic | File | Description |
|-----------------|------|-------------|
| Code style & patterns | `reference/style.md` | Python coding standards, scientific-python conventions, type hints, project structure |

## Package Manager

**Always use `uv` for all package management and tool execution.**

- Install dependencies: `uv python -m pip install <package>` or `uv sync`
- Install in development mode: `uv python -m pip install -e .`
- Run external tools: `uv run <tool>` (e.g., `uv run ruff`, `uv run pytest`)
- Execute scripts: `uv run <script>`

The `uv` package manager should be used consistently for:
- Installing Python packages
- Running development tools (ruff, pytest, etc.)
- Executing project scripts
- Managing virtual environments


## Code Style Highlights

- Type hints required on all functions
- `from __future__ import annotations` for modern syntax
- Google-style docstrings
- Rich console for formatted output
- Dataclasses for configuration
- pathlib.Path for file operations

See `reference/style.md` for complete style guide.

## Style Contracts

**Enforce these style rules in all code. See `reference/style.md` for detailed explanations and examples.**

- Import organization: Standard library → Third-party → Local (grouped, sorted by ruff) - See [Common Problems > I001](reference/style.md#i001-import-sorting)
- All imports at top-level: Never use conditional imports inside functions/blocks - See [Common Problems > PLC0415](reference/style.md#plc0415-conditional-imports)
- Type hints required: All function signatures must include type hints
- Future annotations: Always include `from __future__ import annotations` at top
- Type-checking imports: Third-party imports used only for type hints go in `TYPE_CHECKING` block - See [Common Problems > TC002](reference/style.md#tc002-type-checking-imports)
- Docstrings: Google-style docstrings, ASCII characters only (no Unicode symbols like ×) - See [Common Problems > RUF002](reference/style.md#ruf002-unicode-symbols-in-docstrings)
- Nested if statements: Combine nested if statements when possible using `and` - See [Common Problems > SIM102](reference/style.md#sim102-nested-if-statements)
- Exception handling: Use `contextlib.suppress()` instead of `try-except-pass` - See [Common Problems > SIM105](reference/style.md#sim105-try-except-pass-pattern)
- Exception types: Catch specific exceptions, never bare `Exception` - See [Common Problems > BLE001](reference/style.md#ble001-catching-bare-exception)
- Exception chaining: Use `raise ... from e` when re-raising exceptions in except blocks - See [Common Problems > B904](reference/style.md#b904-exception-chaining)
- Loop variables: Don't overwrite loop variables with assignment - See [Common Problems > PLW2901](reference/style.md#plw2901-loop-variable-overwrite)
- Unnecessary else: Remove `else` after `return` statements - See [Common Problems > RET505](reference/style.md#ret505-unnecessary-else-after-return)
- Path handling: Use `pathlib.Path` instead of `os.path`, use `Path.open()` instead of `open()` - See [Common Problems > PTH123](reference/style.md#pth123-using-open-instead-of-pathopen)
- Dataclass defaults: Use `field(default_factory=...)` for mutable defaults
- Datetime handling: Use timezone-aware datetimes or handle timezone conversion explicitly - See [Common Problems > DTZ007](reference/style.md#dtz007-naive-datetime-construction)

## Git Workflow

- Use conventional commits: `type: description`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.
- Atomic commits with clear, descriptive messages
- Include co-authorship when applicable
