# Confluence Synchronization Reference

## Source of truth

`confluence-pages/` is the local source of truth for published project documentation.

## Synchronization rules

- Synchronize only Markdown under `confluence-pages/`.
- Never synchronize `pm-area/`.
- Reuse existing Confluence pages whenever possible.
- Preserve parent-child hierarchy.
- Use stable page mappings rather than source-document filenames.
- Do not invent page IDs, space keys, parent IDs or URLs.
- Discover the actual connected Atlassian MCP tools and use their runtime schemas.
- If the MCP is unavailable, keep local Markdown changes and report the skipped synchronization.
