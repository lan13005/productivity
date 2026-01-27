# Sync Command

Synchronize references between `.claude/agents.md` and `.claude/reference/style.md` to ensure consistency.

## Goal

Ensure that all style patterns documented in `.claude/agents.md` Style Contracts section have corresponding detailed explanations in `.claude/reference/style.md` Common Problems section, and vice versa. Verify that all cross-references are correct and anchor links work properly.

## Context

The project maintains style documentation in two complementary files:
- `.claude/agents.md`: Contains concise single-line descriptions in the Style Contracts section
- `.claude/reference/style.md`: Contains detailed explanations in the Common Problems section

These files should stay synchronized:
- Every pattern mentioned in `.claude/agents.md` Style Contracts should have a corresponding section in `.claude/reference/style.md` Common Problems
- Every Common Problems section in `.claude/reference/style.md` should be referenced in `.claude/agents.md` Style Contracts (if applicable)
- All anchor links between the files should be valid

## Scope

This command handles:
- Verifying that all Style Contracts items in `.claude/agents.md` have corresponding Common Problems sections
- Verifying that all Common Problems sections are referenced in Style Contracts
- Checking that anchor links are correctly formatted and point to valid sections
- Reporting any missing references or broken links
- Fixing broken anchor links
- Adding missing Style Contracts references for existing Common Problems sections
- Adding missing Common Problems sections for existing Style Contracts references

This command does NOT:
- Modify code files (use `/lint` command for that)
- Run linting or code quality checks (use `/lint` command for that)
- Add new patterns discovered during linting (that's handled by `/lint` command before calling sync)
- Change existing content of style documentation (only adds missing references/sections and fixes broken links)

## Constraints

- Requires read/write access to `.claude/agents.md` and `.claude/reference/style.md` only
- Does NOT require access to code files (this command only modifies documentation)
- Anchor links use lowercase with hyphens (e.g., `#plc0415-conditional-imports`)
- Style Contracts items may reference multiple Common Problems sections
- Some Style Contracts items may not have specific Common Problems sections (general guidelines)
- Only adds content to documentation files - does not modify existing content unless fixing broken references

## Instructions

### Step 1: Read Both Files

1. **Read `.claude/agents.md`**
   - Locate the "Style Contracts" section
   - Extract all items that reference Common Problems (items with "See [Common Problems > ...]" links)
   - Note the rule codes mentioned (e.g., PLC0415, RUF002, SIM105)

2. **Read `.claude/reference/style.md`**
   - Locate the "Common Problems" section
   - Extract all subsection headers (e.g., `### PLC0415: Conditional Imports`)
   - Extract anchor IDs from headers (convert to lowercase with hyphens)
   - Note all rule codes documented

### Step 2: Verify References from agents.md to style.md

For each Style Contracts item that references a Common Problems section:

1. **Check anchor link format**
   - Verify link format: `[Common Problems > RULE_CODE](.claude/reference/style.md#rule-code-description)`
   - Ensure anchor matches the header format in style.md

2. **Verify section exists**
   - Check that the referenced section exists in style.md Common Problems
   - Verify the rule code matches (case-insensitive)
   - Confirm the section has content (not just a header)

3. **Report missing references**
   - If a Style Contracts item references a section that doesn't exist, report it
   - Suggest creating the missing section or removing the reference

### Step 3: Verify References from style.md to agents.md

For each Common Problems section in style.md:

1. **Check if referenced in agents.md**
   - Look for the rule code in Style Contracts section
   - Verify the reference link points back correctly

2. **Report unreferenced sections**
   - If a Common Problems section exists but isn't referenced in Style Contracts, report it
   - Suggest adding a reference or documenting why it's not needed

### Step 4: Verify Anchor Links

1. **Check anchor format consistency**
   - Headers in style.md should use format: `### RULE_CODE: Description`
   - Anchors should be lowercase with hyphens: `#rule-code-description`
   - Links in agents.md should match these anchors exactly

2. **Test anchor validity**
   - Verify that anchor links would resolve correctly
   - Check for special characters that might break anchors
   - Ensure no duplicate anchors exist

### Step 5: Generate Report

1. **Create summary report**
   - List all Style Contracts items with their references
   - List all Common Problems sections
   - Highlight any discrepancies:
     - Missing Common Problems sections
     - Unreferenced Common Problems sections
     - Broken anchor links
     - Format inconsistencies

2. **Provide recommendations**
   - Suggest adding missing sections
   - Suggest adding missing references
   - Suggest fixing broken links
   - Note any intentional omissions (if applicable)

### Step 6: Fix Synchronization Issues

If user approves or if discrepancies are found:

1. **Add missing Style Contracts references**
   - For Common Problems sections that exist but aren't referenced in Style Contracts:
     - Add Style Contracts items following the format: `- Description: Brief description - See [Common Problems > RULE_CODE](.claude/reference/style.md#rule-code-description)`
     - Place in appropriate location within Style Contracts section

2. **Fix broken anchor links**
   - Update anchor links in Style Contracts to match actual section headers in Common Problems
   - Ensure consistent formatting
   - Verify links resolve correctly

3. **Add missing Common Problems sections**
   - For Style Contracts references that point to non-existent Common Problems sections:
     - Create Common Problems sections following the format: `### RULE_CODE: Description`
     - Include:
       - **Problem**: Brief description of the issue
       - **Bad**: Example of incorrect code with `# ❌ RULE_CODE` comment
       - **Good**: Example of correct code with `# ✅` comment
       - **Reference**: Link to related style guidelines if applicable
     - Place new sections in alphabetical order by rule code within Common Problems section
     - Follow the format of existing sections

## Output

The command produces:
- Summary of Style Contracts items and their references
- Summary of Common Problems sections
- List of discrepancies found:
  - Missing Common Problems sections (referenced in Style Contracts but don't exist)
  - Missing Style Contracts references (exist in Common Problems but not referenced)
  - Broken anchor links (links that don't resolve correctly)
- Recommendations for fixing synchronization issues
- Updated documentation files (`.claude/agents.md` and `.claude/reference/style.md`) with synchronized references
- Verification report confirming all references are valid and synchronized

## Expected Pattern Mapping

Common ruff rule codes and their expected sections:

| Rule Code | Section Title | Anchor |
|-----------|---------------|--------|
| PLC0415 | Conditional Imports | `#plc0415-conditional-imports` |
| RUF002 | Unicode Symbols in Docstrings | `#ruf002-unicode-symbols-in-docstrings` |
| SIM105 | try-except-pass Pattern | `#sim105-try-except-pass-pattern` |
| SIM102 | Nested If Statements | `#sim102-nested-if-statements` |
| RET505 | Unnecessary Else After Return | `#ret505-unnecessary-else-after-return` |
| BLE001 | Catching Bare Exception | `#ble001-catching-bare-exception` |
| TC002 | Type-Checking Imports | `#tc002-type-checking-imports` |
| PTH123 | Using open() Instead of Path.open() | `#pth123-using-open-instead-of-pathopen` |
| DTZ007 | Naive Datetime Construction | `#dtz007-naive-datetime-construction` |
| I001 | Import Sorting | `#i001-import-sorting` |

## Examples

### Example: Missing Reference

```
Issue: Common Problems section "PTH123: Using open() Instead of Path.open()" exists in style.md but is not referenced in agents.md Style Contracts.

Recommendation: Add to Style Contracts:
- Path handling: Use `pathlib.Path` instead of `os.path`, use `Path.open()` instead of `open()` - See [Common Problems > PTH123](.claude/reference/style.md#pth123-using-open-instead-of-pathopen)
```

### Example: Broken Anchor Link

```
Issue: Style Contracts references "#sim105-try-except-pass" but style.md section header is "### SIM105: try-except-pass Pattern" which creates anchor "#sim105-try-except-pass-pattern"

Recommendation: Update link in agents.md to match actual anchor:
- Exception handling: Use `contextlib.suppress()` instead of `try-except-pass` - See [Common Problems > SIM105](.claude/reference/style.md#sim105-try-except-pass-pattern)
```

### Example: Missing Section

```
Issue: Style Contracts references "DTZ007" but no corresponding Common Problems section exists in style.md.

Recommendation: Add section to style.md Common Problems:
### DTZ007: Naive Datetime Construction

**Problem**: Creating datetime objects without timezone information...

[Include Bad/Good examples and reference to Error Handling section]
```

### Example: Synchronization Fix

```
Step 6: Fixing synchronization issues

Found discrepancies:
1. Common Problems section "RUF003: Unicode Symbols in Comments" exists but not referenced in Style Contracts
2. Style Contracts references "#sim105-try-except-pass" but actual anchor is "#sim105-try-except-pass-pattern"

Fixing issues:

1. Added Style Contracts reference for RUF003:
   - Comments: Use ASCII characters only (no Unicode symbols like ×) - See [Common Problems > RUF003](.claude/reference/style.md#ruf003-unicode-symbols-in-comments)

2. Fixed broken anchor link for SIM105:
   - Updated: Exception handling: Use `contextlib.suppress()` instead of `try-except-pass` - See [Common Problems > SIM105](.claude/reference/style.md#sim105-try-except-pass-pattern)

Verification: All references are now synchronized ✅

Summary:
- Issues found: 2
- Issues fixed: 2
- Documentation files updated: 1 (.claude/agents.md)
```

## Notes

- Anchor generation: Markdown headers `### RULE_CODE: Description` create anchors by:
  1. Converting to lowercase
  2. Replacing spaces with hyphens
  3. Removing special characters (keeping hyphens)
  4. Example: `### SIM105: try-except-pass Pattern` → `#sim105-try-except-pass-pattern`

- Some Style Contracts items may be general guidelines without specific Common Problems sections (e.g., "Type hints required", "Future annotations")

- The sync process should preserve existing content and only add missing references/sections or fix broken links

- **Documentation-only**: This command ONLY modifies `.claude/agents.md` and `.claude/reference/style.md`. It does NOT modify code files. Use `/lint` command to fix code files.

- **Called by lint command**: This command is automatically called by `/lint` after it adds new patterns to the documentation files. The sync command then verifies that all references are properly synchronized.

- **Synchronization focus**: This command focuses solely on ensuring consistency between the two documentation files - verifying references exist, links work, and both files stay in sync.

- Run this command automatically after linting (via `/lint`) or manually when adding new style patterns to ensure documentation stays synchronized
