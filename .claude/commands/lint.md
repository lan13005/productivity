# Lint Command

Run a four-phase linting process using ruff with progressive fix strategies, manual intervention, and documentation updates.

## Goal

Execute a comprehensive linting workflow that safely applies automatic fixes, carefully evaluates unsafe fixes with human oversight, manually resolves remaining issues, and documents new patterns for future use.

## Context

Ruff provides automatic code fixes at different safety levels. Some fixes are safe and can be applied automatically, while "unsafe" fixes might change code behavior and require review. This command ensures code quality while preventing unintended changes through a staged approach with intervention points.

## Scope

This command handles:
- Running ruff with safe automatic fixes (Phase 1)
- Applying unsafe fixes with diff review and approval (Phase 2)
- Manual analysis and fixing of remaining linting errors (Phase 3)
- Documenting new patterns in style guide files (Phase 4)
- All ruff-supported linting rules for Python code

This command does NOT:
- Handle linters other than ruff
- Modify configuration files (uses existing ruff settings)
- Commit changes automatically

## Constraints

- Requires ruff to be installed and available (use package manager from `.claude/agents.md`)
- Uses project's existing ruff configuration (pyproject.toml or ruff.toml)
- Requires git for diff viewing in Phase 2
- User must approve unsafe fixes before they are applied

## Instructions

### Phase 1: Safe Automatic Fixes

1. **Run ruff with safe fixes**
   ```bash
   uv run ruff check --fix .
   ```
   
   Note: Use the package manager specified in `.claude/agents.md` to run ruff.

2. **Report results**
   - Show summary of fixes applied
   - Note any remaining errors/warnings
   - If no issues remain, inform user and exit

3. **Proceed to Phase 2** if linting errors remain

### Phase 2: Unsafe Fixes with Review

1. **Preview unsafe fixes**
   ```bash
   uv run ruff check --fix --unsafe-fixes --diff .
   ```
   
   Note: Use the package manager specified in `.claude/agents.md` to run ruff.

2. **Analyze the diff critically**
   - Review each proposed change carefully
   - Consider:
     - Does this change code behavior?
     - Could this break existing functionality?
     - Is the fix semantically correct?
     - Are there edge cases that might be affected?
   - Flag any changes that seem questionable or risky

3. **Provide critique to user**
   - Summarize what the unsafe fixes would do
   - Highlight any concerning changes with specific file:line references
   - Note which fixes appear safe vs. which need careful consideration
   - Explain potential risks or side effects

4. **Get user decision**
   - Ask if they want to:
     - Apply all unsafe fixes
     - Apply only specific fixes (specify which)
     - Skip unsafe fixes and proceed to manual fixing
   - If user approves, run:
     ```bash
     uv run ruff check --fix --unsafe-fixes .
     ```
     
     Note: Use the package manager specified in `.claude/agents.md` to run ruff.

5. **Proceed to Phase 3** if linting errors still remain

### Phase 3: Manual Analysis and Fixing

1. **Get remaining errors**
   ```bash
   uv run ruff check .
   ```

   Note: Use the package manager specified in `.claude/agents.md` to run ruff.

2. **Analyze each error**
   - Read the files with errors
   - Understand the context of each issue
   - Determine the correct fix for each error
   - Group similar errors for batch fixing

3. **Fix errors systematically**
   - Use Edit tool to fix issues in each file
   - Follow best practices:
     - Preserve existing code style
     - Don't over-engineer solutions
     - Only change what's necessary to fix the error
     - Ensure fixes align with ruff rule intent
   - **Reference style patterns**: For each linting error, check:
     - `.claude/agents.md` Style Contracts section for concise rule descriptions
     - `.claude/reference/style.md` Common Problems section for detailed explanations and examples
     - Common ruff rule codes (PLC0415, RUF002, SIM105, SIM102, RET505, BLE001, TC002, PTH123, DTZ007, I001) map to specific problem sections
   - **Track new patterns**: Note any linting errors that aren't documented in the style guide for Phase 4

4. **Verify fixes**
   - After fixing each file or group of files, run:
     ```bash
     uv run ruff check .
     ```

     Note: Use the package manager specified in `.claude/agents.md` to run ruff.
   - Confirm errors are resolved
   - Continue until all errors are fixed

5. **Final verification**
   - Run complete ruff check to confirm zero errors:
     ```bash
     uv run ruff check .
     ```

     Note: Use the package manager specified in `.claude/agents.md` to run ruff.
   - Report final linting status to user
   - Proceed to Phase 4 if new patterns were discovered

### Phase 4: Documentation and Synchronization

This phase only runs if new linting patterns were discovered in Phase 3 that aren't documented in the style guide.

1. **Add new patterns to `.claude/agents.md` Style Contracts section**
   - For each new pattern discovered during linting:
     - Add a clear single-line entry to the Style Contracts section (lines 135-152)
     - Format: `- Description: Brief description - See [Common Problems > RULE_CODE](reference/style.md#rule-code-description)`
     - Place in appropriate location within the Style Contracts list
     - Example: `- Path handling: Use pathlib.Path instead of os.path, use Path.open() instead of open() - See [Common Problems > PTH123](reference/style.md#pth123-using-open-instead-of-pathopen)`

2. **Add detailed sections to `.claude/reference/style.md` Common Problems section**
   - For each new pattern discovered during linting:
     - Add a detailed Common Problems section (after line 282)
     - Include:
       - Header: `### RULE_CODE: Description`
       - **Problem**: Brief description of the issue
       - **Bad**: Example of incorrect code with `# ❌ RULE_CODE` comment
       - **Good**: Example of correct code with `# ✅` comment
       - **Reference**: Link to related style guidelines if applicable
     - Place new sections in alphabetical order by rule code within Common Problems section
     - Follow the format of existing sections

3. **Run `/sync` command to verify synchronization**
   - After adding patterns to both files, run the `/sync` command
   - The sync command will verify synchronization between documentation files:
     - All Style Contracts items have corresponding Common Problems sections
     - All Common Problems sections are referenced in Style Contracts
     - Anchor links are correctly formatted and valid
     - All references between files are properly synchronized
   - If sync finds any broken links or missing references, it will fix them
   - Report synchronization status and any fixes applied

4. **Report documentation updates**
   - Summarize all new patterns added to both style guide files
   - List rule codes and descriptions
   - Confirm synchronization status

## Output

The command produces:

**Phase 1:**
- Summary of safe fixes applied
- List of remaining errors (if any)

**Phase 2:**
- Diff critique for unsafe fixes with risk assessment
- User decision on applying unsafe fixes
- Summary of unsafe fixes applied (if approved)

**Phase 3:**
- List of manual fixes applied with file:line references
- Style guide sections referenced for each fix
- Final linting status (zero errors confirmation)
- Modified Python files with all fixes applied

**Phase 4 (only if new patterns discovered):**
- List of new patterns added to `.claude/agents.md` Style Contracts section
- List of new patterns added to `.claude/reference/style.md` Common Problems section
- Synchronization report from `/sync` command
- Confirmation that all documentation is properly synchronized

## Best Practices

- **Always review unsafe fixes**: Never blindly apply `--unsafe-fixes` without reviewing the diff (Phase 2)
- **Understand the rule**: Before fixing, understand why ruff flagged the issue (Phase 3)
  - Check `.claude/agents.md` Style Contracts section for quick reference
  - Consult `.claude/reference/style.md` Common Problems section for detailed explanations
- **Minimal changes**: Only modify code to fix the specific linting error (Phase 3)
- **Preserve intent**: Ensure fixes don't change the original code's intended behavior (Phase 3)
- **Test after**: If changes are significant, suggest running tests (after Phase 3)
- **Track new patterns**: Note any undocumented patterns encountered during Phase 3 for Phase 4
- **Document discoveries**: When new patterns are found, update both style guide files in Phase 4
- **Verify synchronization**: Always run `/sync` after documentation updates to ensure consistency (Phase 4)

## Common Pitfalls

- **Unsafe fixes changing behavior** (Phase 2): Some unsafe fixes might inadvertently change logic - always review the diff
- **Batch applying without review** (Phase 2): Applying all unsafe fixes without reviewing can introduce subtle bugs
- **Over-fixing** (Phase 3): Don't refactor or "improve" code beyond what's needed to fix linting errors
- **Ignoring context** (Phase 3): Some linting errors are intentional; understand the code before changing it
- **Not referencing style guide** (Phase 3): Always check `.claude/agents.md` and `.claude/reference/style.md` before fixing
- **Skipping documentation** (Phase 4): When new patterns are discovered, don't skip Phase 4 - document them for future use
- **Incomplete documentation** (Phase 4): Ensure patterns are added to both `.claude/agents.md` and `.claude/reference/style.md`
- **Not running sync** (Phase 4): Always run `/sync` to verify documentation consistency after updates

## Error Handling

If errors occur:
- **Ruff not installed**: Inform user and suggest installation using the package manager specified in `.claude/agents.md`
- **No ruff config**: Ruff will use defaults; inform user they can add config to pyproject.toml
- **Git not available**: Phase 2 diff preview won't work; suggest viewing changes in IDE
- **Permission errors**: Check file permissions and inform user
- **Syntax errors preventing linting**: Fix syntax errors first, then re-run lint command

## Examples

### Example: Phase 2 Critique

```
Phase 2: Reviewing unsafe fixes

The --unsafe-fixes flag would make the following changes:

1. src/sana/plotting.py:45
   - Removes unused variable 'temp_data'
   - SAFE: Variable is assigned but never used

2. src/sana/utility.py:120
   - Simplifies 'if x == True:' to 'if x:'
   - SAFE: Semantically equivalent, more Pythonic

3. src/sana/config.py:78
   - Removes 'pass' statement in except block
   - CONCERNING: This except block might be intentionally empty for error suppression
   - Suggest: Keep this or replace with explicit comment

Recommendation: Apply fixes #1 and #2, but manually review #3.

Would you like to proceed with all unsafe fixes, or should we handle #3 separately?
```

### Example: Phase 3 Manual Fixes

```
Phase 3: Manual Analysis and Fixing

Found 4 linting errors to fix manually:

1. src/sana/cli.py:221 (PTH123)
   - Issue: Using open() instead of Path.open()
   - Referenced: "PTH123: Using open() Instead of Path.open()" in style guide
   - Fixed: Changed `open(path)` → `path.open()`

2. src/sana/cli.py:225 (PLC0415)
   - Issue: Conditional import inside function
   - Referenced: "PLC0415: Conditional Imports" in style guide
   - Fixed: Moved `import re` to top-level

3. src/sana/plotting.py:2662 (RUF003)
   - Issue: Unicode character in comment
   - Referenced: "RUF002: Unicode Symbols in Docstrings" (similar pattern)
   - Fixed: Replaced `×` with `x` in comment
   - Note: RUF003 not documented - will add in Phase 4

4. src/sana/utility.py:399 (SIM102)
   - Issue: Nested if statements
   - Referenced: "SIM102: Nested If Statements" in style guide
   - Fixed: Combined using `and` operator

Running final verification... ✓ All linting errors resolved

New pattern discovered: RUF003 (Unicode in comments) - proceeding to Phase 4
```

### Example: Phase 4 Documentation

```
Phase 4: Documentation and Synchronization

Adding new pattern RUF003 to style guide files:

1. Updated `.claude/agents.md` Style Contracts:
   - Added: "Comments: Use ASCII characters only in comments (no Unicode) - See [Common Problems > RUF003](reference/style.md#ruf003-unicode-symbols-in-comments)"

2. Updated `.claude/reference/style.md` Common Problems:
   - Added section: "### RUF003: Unicode Symbols in Comments"
   - Included Problem/Bad/Good examples
   - Cross-referenced RUF002 for related pattern

3. Running /sync command... ✓ Synchronization verified
   - All Style Contracts have corresponding Common Problems sections
   - All anchor links valid
   - Documentation is synchronized

Documentation complete: 1 new pattern added and synchronized
```

## Notes

- Ruff is fast; re-running checks between phases is inexpensive
- The four-phase approach provides clear separation of concerns:
  - Phase 1: Automated safe fixes
  - Phase 2: Reviewed unsafe fixes
  - Phase 3: Manual code fixes
  - Phase 4: Documentation updates (only if needed)
- User intervention in Phase 2 is crucial for preventing unintended changes
- Some linting errors might indicate actual bugs; don't just silence them
- Phase 4 only runs when new patterns are discovered, keeping the workflow efficient
- **Documentation workflow** (Phase 4):
  1. Add new patterns to `.claude/agents.md` Style Contracts (single-line entries)
  2. Add detailed sections to `.claude/reference/style.md` Common Problems (with examples)
  3. Run `/sync` command to verify synchronization and fix any broken links
- The documentation phase ensures knowledge from linting sessions is captured for future use
- Phase separation keeps the command modular and maintainable
