# Clean LaTeX in Markdown Command

Format markdown for Obsidian: LaTeX blocks use `$$`, inline uses `$`, remove extra newlines between lists, fix broken LaTeX.

## Fixes

- Delimiters: `\[`/`\]` → `$$`, `\(`/`\)` → `$` (use `replace_all=true`)
- Broken patterns: `*` → `_` in subscripts, `;` → `,` in sets, fix missing `\` in line breaks
- List spacing: Remove double newlines between numbered/bullet lists and nested items (`^\d+\. .*\n\n   \*` → `^\d+\. .*\n   \*`, `^\* .*\n\n   \*` → `^\* .*\n   \*`)
