# Document Processing Reference

## Processing stages

1. Discover files in `uncategorized/`.
2. Read all relevant source documents.
3. Classify each source into the project taxonomy.
4. Move source files into the matching folder under `source-documents/` without changing their original format/content.
5. Register each moved file in `pm-area/source-map.md` (relative path, added date, updated date).
6. Compare extracted information with existing project knowledge.
7. Update or create canonical Markdown pages in `confluence-pages/`.
8. Update or create internal Markdown in `pm-area/` when needed.
9. Detect conflicts and unresolved questions.
10. Synchronize affected Confluence pages only.
11. Report changes and unresolved items.

## Language

Before step 7, make sure `project.language` is set in `project.yaml` (ask the user if not). Write all pages in that language, keeping technical/PM/software terms in English.

## Do not use one-to-one mapping

A source file is not automatically a Markdown page. A single source can contribute to multiple canonical pages, and multiple sources can contribute to one canonical page.

## Email threads

Email thread files (`.eml`, `.msg`, exported threads) are converted to readable Markdown (`scripts/eml_to_md.py` for `.eml`) and only the `.md` is stored in `pm-area/emails/`; the original email file is deleted from `uncategorized/` after the `.md` is checked. They are not registered in `source-map.md`. If a thread looks like an official source document (signed approval, formal decision, contractual confirmation), ask the user to confirm before moving it into `source-documents/`. Attachments are extracted first (`scripts/eml_to_md.py` does this) to `uncategorized/attachments/<email-md-name>/`, then classified: suitable project documents move to `source-documents/` and are registered in `source-map.md`; unsuitable ones are deleted only after the user confirms; unclear ones stay in `uncategorized/attachments/`. The original email file is deleted only after the `.md` and all attachments are in place. In headless runs, never delete; classify only clear-cut attachments and report the rest.

## Source paths

Reference sources by path relative to `source-documents/`, without that prefix.

## Unsupported or ambiguous classification

If the assistant cannot confidently classify a document, leave it in `uncategorized/` and ask for clarification or report the reason. Do not create a speculative category. Files left in the inbox are not added to `source-map.md`.
