# Lint Command

Four-phase ruff linting: safe fixes, unsafe fixes with review, manual fixes, documentation updates.

## Instructions

### Phase 1: Safe Automatic Fixes
1. Run `uv run ruff check --fix .`
2. Report fixes applied, remaining errors
3. Exit if no issues, else proceed to Phase 2

### Phase 2: Unsafe Fixes with Review
1. Preview: `uv run ruff check --fix --unsafe-fixes --diff .`
2. Analyze diff: Check behavior changes, breakage risk, semantic correctness, edge cases
3. Critique: Summarize fixes, highlight concerns with file:line, note safe vs risky
4. Get approval: Apply all/specific/skip unsafe fixes
5. If approved: `uv run ruff check --fix --unsafe-fixes .`
6. Proceed to Phase 3 if errors remain

### Phase 3: Manual Analysis and Fixing
1. Get errors: `uv run ruff check .`
2. Analyze: Read files, understand context, determine fixes, group similar errors
3. Fix systematically:
   - Use Edit tool, preserve style, minimal changes, align with rule intent
   - Reference: `.claude/agents.md` Style Contracts, `.claude/reference/style.md` Common Problems
   - Track new patterns for Phase 4
4. Verify: Run `uv run ruff check .` after each file/group
5. Final: Confirm zero errors, proceed to Phase 4 if new patterns found

### Phase 4: Documentation (only if new patterns discovered)
1. Add to `.claude/agents.md` Style Contracts: Single-line entry with format `- Description: Brief - See [Common Problems > RULE_CODE](reference/style.md#rule-code-description)`
2. Add to `.claude/reference/style.md` Common Problems: Section with `### RULE_CODE: Description`, Problem/Bad/Good examples, alphabetical order
3. Run `/sync` to verify synchronization
4. Report: Summarize new patterns, rule codes, sync status

## Constraints

- Requires ruff (use package manager from `.claude/agents.md`)
- Uses existing ruff config
- Git needed for Phase 2 diff
- User must approve unsafe fixes

## Best Practices

- Always review unsafe fixes (Phase 2)
- Understand rule before fixing (Phase 3): Check Style Contracts, Common Problems
- Minimal changes, preserve intent (Phase 3)
- Track new patterns (Phase 3)
- Document discoveries, verify sync (Phase 4)

## Common Pitfalls

- Unsafe fixes changing behavior: Review diff (Phase 2)
- Over-fixing: Only fix linting errors (Phase 3)
- Ignoring context: Understand code before changing (Phase 3)
- Not referencing style guide: Check both files (Phase 3)
- Skipping documentation: Document new patterns (Phase 4)
- Not running sync: Verify consistency (Phase 4)

## Error Handling

- Ruff not installed: Suggest installation
- No config: Uses defaults, can add to pyproject.toml
- Git unavailable: Phase 2 diff won't work, use IDE
- Permission errors: Check file permissions
- Syntax errors: Fix first, then re-run

## Notes

- Four phases: Safe fixes → Reviewed unsafe → Manual → Documentation (if needed)
- Phase 4 only runs when new patterns discovered
- Documentation workflow: Add to Style Contracts → Add to Common Problems → Run `/sync`
