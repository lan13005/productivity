# Python Coding Style Guide

This project follows scientific Python ecosystem best practices and patterns.

## Project Structure

### Layout
- Use `src/` layout with package code in `src/jdsp/`
- Single `pyproject.toml` as source of truth (SPEC 0 compliant)
- Tests in `tests/` directory
- Documentation in `docs/` directory (if present)

### Build System
- Use modern build backends: `hatchling` or `setuptools-scm`
- Follow PEP 621 for project metadata in `pyproject.toml`
- Specify `requires-python` constraint explicitly
- Pin minimum dependency versions in `dependencies` array

## Code Organization

### Imports
- Always include `from __future__ import annotations` at the top
- **All imports must be at top-level**: Never use conditional imports inside functions or blocks
- Group imports in three sections:
  1. Standard library
  2. Third-party packages
  3. Local/project imports
- Use absolute imports for project modules
- **Type-checking imports**: Third-party imports used only for type hints should be placed in `TYPE_CHECKING` block
- Ruff automatically sorts imports (I001 rule) - run `ruff check --fix` to format
- Example from cli.py:
  ```python
  from __future__ import annotations

  import argparse
  import json
  import sys
  from pathlib import Path
  from typing import TYPE_CHECKING, Any, Dict, List, Tuple

  import pandas as pd
  from rich.console import Console

  from jdsp.plotting import plot_efficiency_avg, ...

  if TYPE_CHECKING:
      from rich.console import Console  # Only if used for type hints
  ```

### Type Hints
- **Required**: All function signatures must include type hints
- Use modern syntax enabled by `from __future__ import annotations`
- Use `|` for union types instead of `Union` (e.g., `int | None`)
- Examples from codebase:
  ```python
  def jains_fairness_index(values: List[float]) -> Tuple[float | None, int | None]:
      """Calculate Rescaled Jain's Fairness Index."""
      ...

  def load_and_filter_data(
      input_file: str,
      days: int | None = None,
      start_date: str | None = None,
      end_date: str | None = None,
  ) -> pd.DataFrame:
      """Load CSV and apply date filters if specified."""
      ...
  ```

## Naming Conventions

- **Functions/variables**: `snake_case` (e.g., `load_and_filter_data`, `cpu_efficiency`)
- **Classes**: `PascalCase` (e.g., `PlotConfig`, `Console`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_CONFIG`, `MAX_USERS`)
- **Private/internal**: Prefix with `_` (e.g., `_internal_helper`)

## Documentation

### Docstrings
- Use Google-style docstrings
- Include brief summary on first line
- Add `Args:` section for parameters (when helpful)
- Add `Returns:` section for return values
- **Use ASCII characters**: Avoid Unicode symbols like `×` (MULTIPLICATION SIGN) - use `x` instead
- Example from cli.py:41-50:
  ```python
  def jains_fairness_index(values: List[float]) -> Tuple[float | None, int | None]:
      """Calculate Rescaled Jain's Fairness Index.

      Computes the standard Jain's Fairness Index (range [1/n, 1]) and rescales it to [0, 1]
      using affine transformation: rescaled = (original - 1/n) / (1 - 1/n).

      Returns:
          tuple: (rescaled_jfi, n) where rescaled_jfi is in [0, 1] and n is the number of values.
                 Returns (None, None) if n < 2 or sum of values is 0.
      """
  ```

### Module Docstrings
- First line of every module should be a docstring
- Example from cli.py:2:
  ```python
  """CLI program to generate diagnostic plots for job defense shield analysis."""
  ```

## Data Classes

- Use `@dataclass` decorator for configuration/data containers
- Import from `dataclasses` module
- Use `field(default_factory=...)` for mutable defaults
- Example from config.py:9-61:
  ```python
  from dataclasses import dataclass, field

  @dataclass
  class PlotConfig:
      """Configuration settings for JDSP plots."""

      max_users_display: int = 30
      figure_dpi: int = 150
      cpu_thresholds: Dict[Tuple[str, str], Tuple[int, int]] = field(
          default_factory=lambda: {
              ("Low", "value"): (0, 8),
              ("Medium", "value"): (8, 32),
          }
      )
  ```

## Error Handling

### User-Facing Errors
- Use `rich.console.Console` for formatted output
- Clear, explicit error messages with color coding:
  - `[red]ERROR:[/red]` for errors
  - `[yellow]WARNING:[/yellow]` for warnings
  - `[dim]...[/dim]` for less important info
  - `[bold green]...[/bold green]` for success
- Example from cli.py:118, 149:
  ```python
  console = Console()

  if not Path(input_file).exists():
      console.print(f"[red]ERROR:[/red] Input file '{input_file}' does not exist.")
      sys.exit(1)

  try:
      start_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
  except ValueError:
      console.print("[red]ERROR:[/red] Invalid start-date format. Use YYYY-MM-DD")
      sys.exit(1)
  ```

### Internal Errors
- Use standard Python exceptions with descriptive messages
- **Catch specific exceptions**: Never catch bare `Exception` - use specific exception types
- Prefer `contextlib.suppress()` over `try-except-pass` when ignoring specific exceptions
- Only use broad exception handling when absolutely necessary, and use specific base classes like `OSError`, `ValueError`

## Path Handling

- Use `pathlib.Path` instead of `os.path`
- Use `Path.open()` instead of `open()` when working with Path objects
- Example from cli.py:117, 320-321:
  ```python
  from pathlib import Path

  if not Path(input_file).exists():
      console.print(f"[red]ERROR:[/red] Input file '{input_file}' does not exist.")

  output_dir = Path(args.output_dir)
  output_dir.mkdir(parents=True, exist_ok=True)
  
  # Good: Use Path.open()
  with Path(file_path).open() as f:
      content = f.read()
  
  # Bad: Don't use open() with Path
  with open(file_path) as f:  # ❌ PTH123
      content = f.read()
  ```

## Dependencies

### Specification
- List all dependencies in `pyproject.toml` under `[project]` → `dependencies`
- Pin minimum versions: `"package>=X.Y.Z"`
- Optional dependencies in `[project.optional-dependencies]`
- Example from pyproject.toml:6-16:
  ```toml
  requires-python = ">=3.14"
  dependencies = [
      "matplotlib>=3.10.8",
      "numpy>=2.4.1",
      "pandas>=2.3.3",
      "rich>=14.2.0",
  ]
  ```

### Entry Points
- Define CLI scripts in `[project.scripts]`
- Example from pyproject.toml:18-19:
  ```toml
  [project.scripts]
  jdsp = "jdsp.cli:main"
  ```

## Code Quality Tools

### Linting and Formatting
- **Ruff**: Primary linter and formatter
  - Fast, comprehensive replacement for flake8, isort, pyupgrade
  - Configuration in `pyproject.toml` under `[tool.ruff]`
  - Run `uv run ruff check --fix .` to auto-fix issues
  - See `.claude/agents.md` Style Contracts section for specific rules enforced

### Type Checking
- **mypy**: Static type checker
  - Run in strict mode
  - Configuration in `pyproject.toml` under `[tool.mypy]`

### Testing
- **pytest**: Testing framework
  - Tests in `tests/` directory
  - Use descriptive test names: `test_<function>_<scenario>`
  - Configuration in `pyproject.toml` under `[tool.pytest.ini_options]`

## General Principles

1. **Explicit is better than implicit**: Clear variable names, explicit error messages
2. **Don't repeat yourself**: Extract common logic into functions
3. **Keep functions focused**: Each function should do one thing well
4. **Use standard library**: Prefer stdlib solutions over third-party when reasonable
5. **Performance**: Use pandas/numpy vectorized operations over loops when possible
6. **Readability**: Code is read more often than written

## Examples from Codebase

### Good Patterns

1. **Type-hinted function with clear docstring** (cli.py:110-115):
   ```python
   def load_and_filter_data(
       input_file: str,
       days: int | None = None,
       start_date: str | None = None,
       end_date: str | None = None,
   ) -> pd.DataFrame:
       """Load CSV and apply date filters if specified."""
   ```

2. **Rich console formatting** (cli.py:121, 269-271):
   ```python
   console.print(f"[dim]Loading data from[/dim] {input_file}...")
   console.print(
       f"[dim]Computed efficiency metrics for[/dim] {df['cpu_eff'].notna().sum()} [dim]jobs with valid data[/dim]"
   )
   ```

3. **Dataclass configuration** (config.py:9-20):
   ```python
   @dataclass
   class PlotConfig:
       """Configuration settings for JDSP plots."""

       max_users_display: int = 30
       figure_dpi: int = 150
       default_figsize: Tuple[int, int] = (14, 8)
   ```

4. **Path handling** (cli.py:320-322):
   ```python
   output_dir = Path(args.output_dir)
   output_dir.mkdir(parents=True, exist_ok=True)
   console.print(f"[dim]Output directory:[/dim] {output_dir}")
   ```

---

## Common Problems

This section documents specific linting errors, code quality issues, and anti-patterns that should be avoided. Each problem includes the ruff rule code (if applicable), examples of bad and good patterns, and references to related style guidelines.

### PLC0415: Conditional Imports

**Problem**: Imports should be at the top-level of a file, not inside functions or conditional blocks.

**Bad**:
```python
def some_function():
    if condition:
        import re  # ❌ PLC0415
        match = re.match(...)
```

**Good**:
```python
import re  # ✅

def some_function():
    if condition:
        match = re.match(...)
```

**Reference**: See [Code Organization > Imports](#code-organization) for import organization guidelines.

---

### RUF002: Unicode Symbols in Docstrings

**Problem**: Docstrings should use ASCII characters only. Unicode symbols like `×` (MULTIPLICATION SIGN) should be replaced with ASCII equivalents.

**Bad**:
```python
"""Sum of (cores × limit_hours)"""  # ❌ RUF002
```

**Good**:
```python
"""Sum of (cores x limit_hours)"""  # ✅
```

**Reference**: See [Documentation > Docstrings](#documentation) for docstring guidelines.

---

### SIM105: try-except-pass Pattern

**Problem**: Using `try-except-pass` to silently ignore exceptions is discouraged. Use `contextlib.suppress()` instead for better clarity.

**Bad**:
```python
try:
    value = float(string_value)
except ValueError:
    pass  # ❌ SIM105
```

**Good**:
```python
import contextlib

with contextlib.suppress(ValueError):
    value = float(string_value)  # ✅
```

**Reference**: See [Error Handling > Internal Errors](#error-handling) for exception handling guidelines.

---

### SIM102: Nested If Statements

**Problem**: Nested `if` statements can often be combined using `and` for better readability.

**Bad**:
```python
if condition1:
    if condition2:
        do_something()  # ❌ SIM102
```

**Good**:
```python
if condition1 and condition2:
    do_something()  # ✅
```

---

### RET505: Unnecessary Else After Return

**Problem**: When an `if` block returns, the `else` clause is unnecessary and can be removed.

**Bad**:
```python
if condition:
    return value1
else:
    return value2  # ❌ RET505
```

**Good**:
```python
if condition:
    return value1
return value2  # ✅
```

---

### B904: Exception Chaining

**Problem**: When re-raising exceptions in an `except` block, use `raise ... from e` or `raise ... from None` to properly chain exceptions and distinguish them from errors in exception handling.

**Bad**:
```python
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    raise ValueError(f"Failed to read CSV: {e}")  # ❌ B904
```

**Good**:
```python
try:
    df = pd.read_csv(csv_path)
except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as e:
    raise ValueError(f"Failed to read CSV: {e}") from e  # ✅
```

**Reference**: See [Error Handling > Internal Errors](#error-handling) for exception handling guidelines.

---

### BLE001: Catching Bare Exception

**Problem**: Catching bare `Exception` is too broad and can hide bugs. Always catch specific exception types.

**Bad**:
```python
try:
    result = subprocess.run(...)
except Exception as e:  # ❌ BLE001
    handle_error(e)
```

**Good**:
```python
try:
    result = subprocess.run(...)
except (OSError, ValueError) as e:  # ✅
    handle_error(e)
```

**Reference**: See [Error Handling > Internal Errors](#error-handling) for exception handling guidelines.

---

### TC002: Type-Checking Imports

**Problem**: Third-party imports used only for type hints should be placed in a `TYPE_CHECKING` block to avoid runtime import overhead.

**Bad**:
```python
from typing import TYPE_CHECKING
import pandas as pd  # Imported but only used in type hints

def process_data(data: pd.DataFrame) -> None:  # ❌ TC002
    ...
```

**Good**:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd  # ✅

def process_data(data: pd.DataFrame) -> None:
    ...
```

**Reference**: See [Code Organization > Imports](#code-organization) for import organization guidelines.

---

### PTH123: Using open() Instead of Path.open()

**Problem**: When working with `pathlib.Path` objects, use `Path.open()` instead of the built-in `open()` function.

**Bad**:
```python
from pathlib import Path

path = Path("file.txt")
with open(path) as f:  # ❌ PTH123
    content = f.read()
```

**Good**:
```python
from pathlib import Path

path = Path("file.txt")
with path.open() as f:  # ✅
    content = f.read()
```

**Reference**: See [Path Handling](#path-handling) for path handling guidelines.

---

### DTZ007: Naive Datetime Construction

**Problem**: Creating datetime objects without timezone information can lead to timezone-related bugs. Use timezone-aware datetimes or explicitly handle timezone conversion.

**Bad**:
```python
from datetime import datetime

date = datetime.strptime("2025-01-01", "%Y-%m-%d")  # ❌ DTZ007
```

**Good**:
```python
from datetime import datetime, timezone

# Option 1: Use timezone-aware datetime
date = datetime.strptime("2025-01-01", "%Y-%m-%d").replace(tzinfo=timezone.utc)

# Option 2: If only date is needed, use date() method
date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
```

**Note**: If you're only extracting the date portion (using `.date()`), the DTZ007 warning may be acceptable, but consider using timezone-aware datetimes if the code will be used across timezones.

---

### I001: Import Sorting

**Problem**: Imports should be organized and sorted according to project conventions (standard library → third-party → local).

**Note**: This is automatically fixed by ruff. Run `uv run ruff check --fix .` to auto-format imports.

**Reference**: See [Code Organization > Imports](#code-organization) for import organization guidelines.

---

### PLW2901: Loop Variable Overwrite

**Problem**: Overwriting a loop variable with an assignment inside the loop body can lead to bugs and confusion. Use a different variable name instead.

**Bad**:
```python
for job_id, job_df in df.groupby("job_id"):
    job_df = job_df.sort_values("time")  # ❌ PLW2901
    # job_df now refers to sorted dataframe, not original group
```

**Good**:
```python
for job_id, job_df in df.groupby("job_id"):
    sorted_job_df = job_df.sort_values("time")  # ✅
    # Use sorted_job_df for sorted operations
```

**Reference**: See [Code Organization](#code-organization) for code organization guidelines.
