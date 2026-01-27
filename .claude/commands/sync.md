# Sync Command

Synchronize references between `.claude/agents.md` Style Contracts and `.claude/reference/style.md` Common Problems. Verify cross-references and anchor links.

## Instructions

### Step 1: Read Both Files
- Read `.claude/agents.md`: Extract Style Contracts items with "See [Common Problems > ...]" links, note rule codes
- Read `.claude/reference/style.md`: Extract Common Problems subsection headers, convert to anchor IDs (lowercase-hyphens), note rule codes

### Step 2: Verify agents.md → style.md
For each Style Contracts reference:
- Check link format: `[Common Problems > RULE_CODE](reference/style.md#rule-code-description)`
- Verify section exists in style.md, rule code matches, section has content
- Report missing references

### Step 3: Verify style.md → agents.md
For each Common Problems section:
- Check if referenced in Style Contracts, verify link points correctly
- Report unreferenced sections

### Step 4: Verify Anchor Links
- Headers: `### RULE_CODE: Description` → anchors: `#rule-code-description` (lowercase-hyphens)
- Links in agents.md must match anchors exactly
- Check for special characters, duplicates

### Step 5: Generate Report
- List Style Contracts items and references
- List Common Problems sections
- Highlight discrepancies: missing sections, unreferenced sections, broken links, format issues
- Provide recommendations

### Step 6: Fix Issues
If discrepancies found:
1. Add missing Style Contracts references: Format `- Description: Brief - See [Common Problems > RULE_CODE](reference/style.md#rule-code-description)`
2. Fix broken anchor links: Update to match actual section headers
3. Add missing Common Problems sections: Format `### RULE_CODE: Description` with Problem/Bad/Good examples, alphabetical order

## Constraints

- Only modifies `.claude/agents.md` and `.claude/reference/style.md` (documentation-only)
- Anchor format: lowercase-hyphens (e.g., `#plc0415-conditional-imports`)
- Some Style Contracts items may not have Common Problems sections (general guidelines)
- Only adds content, doesn't modify existing content (except fixing broken links)

## Common Rule Codes

PLC0415, RUF002, SIM105, SIM102, RET505, BLE001, TC002, PTH123, DTZ007, I001, PLW2901

## Notes

- Anchor generation: `### RULE_CODE: Description` → `#rule-code-description` (lowercase, spaces→hyphens)
- Preserve existing content, only add missing references/sections or fix broken links
- Called by `/lint` after adding new patterns
- Run after linting or when adding new style patterns
