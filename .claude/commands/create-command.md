# Create-Command Command

Create or update command files documenting workflows and best practices from problem/solution analysis. Convert markdown files to command format when referenced.

## Instructions

### Creating from Context

1. **Analyze Context**: Review conversation history, open files, recent edits. Identify problems, solutions, mistakes.
2. **Extract Problem/Solution Pairs**: Document what, how, why, prevention for each problem.
3. **Document Best Practices**: Extract patterns, workflows, pitfalls, validation steps.
4. **Create Structure**: Write `.claude/commands/<name>.md` with sections:
   - `# <Command Name> Command` + brief description
   - `## Goal`: Clear objective
   - `## Context`: Background, when to use, problems addressed
   - `## Scope`: Boundaries
   - `## Constraints`: Prerequisites, limitations
   - `## Instructions`: Step-by-step workflow
   - `## Output`: Expected results
   - Optional: Common Pitfalls, Best Practices, Validation Steps, Error Handling
5. **Fill Sections**: Use problem/solution analysis to populate each section.
6. **Save**: Write file, verify by reading back.

### Converting Markdown File

**CRITICAL: Do NOT enter plan mode. Transform immediately.**

1. **Read file NOW**: Use Read tool to get complete content.
2. **Transform immediately**: Use Write/Edit tool to restructure:
   - Extract Goal from intro
   - Organize background → Context
   - Define boundaries → Scope
   - Document limitations → Constraints
   - Convert procedures → Instructions
   - Specify results → Output
   - Preserve all valuable content
   - Ask if file should move to `.claude/commands/` if elsewhere
3. **Enhance**: Extract problems/issues into Common Pitfalls, document solutions, add best practices.
4. **Verify**: Ensure standard sections present, formatting consistent, content preserved.
5. **Inform**: Confirm update, note changes.

## Constraints

- Save in `.claude/commands/`, lowercase-hyphen names
- Follow standard structure
- Preserve valuable content when updating
- Focus on actionable problem/solution pairs

## Security

- Never: Overwrite without confirmation (except referenced file updates), include sensitive info, lose original content
- Always: Verify paths, preserve content, add safety warnings, document prerequisites, ask before moving files

## Error Handling

- File exists: Ask update or different name
- Invalid name: Suggest lowercase-hyphen format
- Missing info: Analyze deeper or ask user
- Permission denied: Check directory permissions
- Malformed: Fix structure
- Cannot read: File doesn't exist or inaccessible

## Notes

- When converting: Transform IMMEDIATELY, no plan mode, no descriptions, just update file
- Analyze for: Error messages, solutions, patterns, mistakes, validation checks
- Commands: Self-contained, clear actionable language, guide behavior not replace it
- Always verify file created/updated by reading back
