# Commit Command

Automate git commits with conventional commit messages, change analysis, and safety checks.

## Instructions

### 1. Review State (parallel)
- `git status`
- `git diff HEAD`
- `git status --porcelain`
- Never use `git status -uall` (memory issues)

### 2. Analyze Changes
- Identify modified/added/deleted files
- Review code changes in `git diff HEAD`
- Determine commit type: `feat`, `fix`, `agent`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`
- Safety checks: warn on secrets, files >10MB, binaries, `.gitignore` files

### 3. Generate Message
Format: `<type>: <description>\n\n[body]\n\nCo-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>`
- Description <72 chars, lowercase, explain why not just what
- Suggest splitting unrelated changes
- Ask user if type unclear

### 4. Stage and Commit
```bash
git add <files>
git commit -m "$(cat <<'EOF'
<type>: <description>

<body>

Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
git status
```

### 5. Confirm
- Show `git status`, commit hash, message, committed files

## Constraints

- Never: `git status -uall`, commit `.gitignore` files, use `--no-verify`, commit sensitive files
- Never commit: `.env`, `credentials.json`, API keys, `__pycache__/`, `*.pyc`, `.DS_Store`, large binaries
- Warn on: secrets, files >10MB, binaries

## Error Handling

- Pre-commit hook fails: Fix and create new commit (never `--no-verify`)
- Nothing to commit: Show status
- Merge conflicts: Prompt user to resolve
- Detached HEAD: Warn user
