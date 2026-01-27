# Clean LaTeX in Markdown Command

Given a set of markdown files we MUST format it for Obsidian markdown so that:
- Latex blocks use `$$`
- Inline latex uses `$`
- No additional new line between lists, limiting vertical spacing usage.
- Fix all broken latex code to conform with Obsidian markdown

## Quick Fixes

**Delimiter conversions:**
- `\[`/`\]` → `$$`
- `\(`/`\)` → `$`
- Use `replace_all=true` for bulk replacements

**Common broken LaTeX patterns:**
- `*` instead of `_` in subscripts: `\mathbf{v}*i` → `\mathbf{v}_i`
- `;` instead of `,` in sets: `{a,; b}` → `\{a, b\}`
- Missing `\` in line breaks: `\\` → `\\`

**List spacing:**
- Pattern: `^\d+\. .*\n\n   \*` → `^\d+\. .*\n   \*`
- Pattern: `^\* .*\n\n   \*` → `^\* .*\n   \*`

**Python one-liner for list spacing:**
```python
re.sub(r'(\d+\. .+?)\n\n   (\*)', r'\1\n   \2', content)
re.sub(r'(\* .+?)\n\n   (\*)', r'\1\n   \2', content)
```