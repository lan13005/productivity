# Commit Command

Automate the git commit workflow with conventional commit messages.

## Goal

Create git commits following conventional commit standards with proper message formatting, change analysis, and safety checks.

## Context

This command automates the git commit process when users invoke `/commit` or request a commit. It ensures:
- Changes are properly analyzed before committing
- Commit messages follow conventional commit format
- Safety checks prevent committing sensitive or inappropriate files
- Commits include proper attribution and clear descriptions

Use this command whenever the user wants to commit changes to the repository.

## Scope

This command covers:
- Analyzing repository state and changes
- Generating conventional commit messages
- Staging files and creating commits
- Validating commit success
- Safety checks for sensitive files

This command does NOT cover:
- Pushing commits to remote repositories
- Resolving merge conflicts (warns user instead)
- Creating branches or tags
- Amending or modifying existing commits

## Constraints

**Prerequisites**:
- Git repository must be initialized
- User must have write access to the repository
- Changes must exist to commit

**Limitations**:
- Never use `git status -uall` (can cause memory issues on large repositories)
- Never commit files in `.gitignore`
- Never use `--no-verify` to bypass pre-commit hooks
- Never commit sensitive files (see Security and Safety section)

**Required Format**:
- Commit messages must follow conventional commit format
- Messages must include Co-authored-by attribution
- Description must be under 72 characters
- Use HEREDOC syntax for multi-line commit messages

## Instructions

### 1. Review Current State

Run these commands **in parallel** to understand the current repository state:

```bash
# Show working tree status
git status

# Show all changes (staged and unstaged)
git diff HEAD

# List files with status
git status --porcelain
```

**Important**: Never use `git status -uall` as it can cause memory issues on large repositories.

### 2. Analyze Changes

Based on the output from step 1:

- Identify all modified, added, and deleted files
- Review the actual code changes in `git diff HEAD`
- Determine the appropriate conventional commit type:
  - `feat:` - New feature or functionality
  - `fix:` - Bug fix
  - `agent:` - Agent-specific (claude, cursor) changes
  - `docs:` - Documentation changes
  - `style:` - Code style/formatting only
  - `refactor:` - Code refactoring without behavior change
  - `test:` - Adding or updating tests
  - `chore:` - Maintenance, dependencies, tooling
  - `perf:` - Performance improvements

See `.claude/reference/git.md` for complete commit type reference.

**Safety Checks**:
- Warn if attempting to commit files that likely contain secrets
- Warn if files are larger than 10MB
- Warn if committing binary files (unless explicitly requested)
- Never commit files in `.gitignore`

### 3. Generate Commit Message

Create a commit message following the conventional commit format:

```
<type>: <description>

[optional body if needed]

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Guidelines**:
- Keep description under 72 characters
- Use lowercase for type and description (unless proper noun)
- Be specific and descriptive
- Explain **why** the change was made, not just what
- If multiple unrelated changes, suggest splitting into separate commits
- ALWAYS analyze changes thoroughly before generating commit message
- The commit message should reflect the **intent** and **impact** of changes
- If unsure about the appropriate commit type, ask the user
- For large changesets, suggest splitting into multiple logical commits

### 4. Stage and Commit

**Sequential operations** (must run in order):

```bash
# Stage all relevant files
git add <file1> <file2> ...

# Create commit with message
git commit -m "$(cat <<'EOF'
<type>: <description>

<optional body>

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Verify commit was created
git status
```

**Important**: Use HEREDOC syntax for commit messages to ensure proper formatting.

### 5. Confirm Success

After committing:
- Show the final `git status` output
- Display the commit hash and message
- Confirm which files were committed

## Output

After execution, the command produces:

1. **Commit Created**: A git commit with conventional commit message format
2. **Status Confirmation**: Final `git status` showing clean working tree (or remaining uncommitted changes)
3. **Commit Details**: Commit hash and full commit message displayed
4. **File Summary**: List of files that were committed

If no changes exist or commit fails, appropriate error messages are displayed.

## Examples

### Simple Feature Addition

```bash
git add src/sana/plotting.py
git commit -m "$(cat <<'EOF'
feat: add GPU memory uniformity plots

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Bug Fix with Context

```bash
git add src/sana/cli.py
git commit -m "$(cat <<'EOF'
fix: handle missing admincomment field gracefully

Previously raised KeyError when admincomment was missing.
Now skips jobs with empty admincomment and continues processing.

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Multiple Files

```bash
git add src/sana/config.py src/sana/plotting.py README.md
git commit -m "$(cat <<'EOF'
feat: add configurable plot thresholds

Moved threshold definitions to config.py for easier customization.
Updated README with threshold configuration examples.

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## Security and Safety

**Never commit**:
- Sensitive files (`.env`, `credentials.json`, API keys)
- Generated files (`__pycache__/`, `*.pyc`, `.DS_Store`)
- Large binary files without user confirmation
- Files in `.gitignore`

**Warn the user** if attempting to commit:
- Files that likely contain secrets
- Files larger than 10MB
- Binary files (unless explicitly requested)

## Error Handling

If errors occur:

- **Pre-commit hook fails**: Fix the issue and create a NEW commit (never use `--no-verify`)
- **Nothing to commit**: Inform user and show current status
- **Merge conflicts**: Prompt user to resolve conflicts first
- **Detached HEAD**: Warn user about repository state
