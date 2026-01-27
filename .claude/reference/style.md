# Python Coding Style Guide

Scientific Python ecosystem best practices.

## Project Structure

- `src/` layout with package code in `src/jdsp/`
- Single `pyproject.toml` (SPEC 0 compliant)
- Tests in `tests/`, docs in `docs/` (if present)
- Build: `hatchling` or `setuptools-scm`, PEP 621 metadata
- Pin minimum dependency versions

## Code Organization

### Imports
- `from __future__ import annotations` at top
- All imports at top-level (no conditional imports)
- Group: stdlib → third-party → local
- Type-checking imports in `TYPE_CHECKING` block
- Ruff sorts automatically (I001)

### Type Hints
- Required on all functions
- Use `|` for unions (`int | None`)
- Modern syntax via `from __future__ import annotations`

## Naming

- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix with `_`

## Documentation

- Google-style docstrings
- ASCII only (no Unicode symbols)
- Module docstring on first line

## Data Classes

- Use `@dataclass` for config/containers
- `field(default_factory=...)` for mutable defaults

## Error Handling

- User-facing: `rich.console.Console` with color codes
- Internal: specific exceptions, `contextlib.suppress()` over `try-except-pass`
- Chain exceptions: `raise ... from e`

## Path Handling

- Use `pathlib.Path` instead of `os.path`
- Use `Path.open()` instead of `open()`

## Dependencies

- List in `pyproject.toml` under `[project]` → `dependencies`
- Pin minimum versions: `"package>=X.Y.Z"`
- Optional deps in `[project.optional-dependencies]`
- CLI scripts in `[project.scripts]`

## Code Quality Tools

- **Ruff**: Primary linter/formatter (`uv run ruff check --fix .`)
- **mypy**: Type checker (strict mode)
- **pytest**: Tests in `tests/`, names: `test_<function>_<scenario>`

## Principles

1. Explicit over implicit
2. DRY: extract common logic
3. Single responsibility per function
4. Prefer stdlib when reasonable
5. Vectorize pandas/numpy operations
6. Readability matters
