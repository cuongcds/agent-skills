# confluence-project-assistant

A Claude Code skill for project documentation lifecycle management.

It keeps a project's documentation in three layers and keeps them in sync with Confluence:

| Layer | Purpose |
| --- | --- |
| `source-documents/` | Original files (DOCX, XLSX, PPTX, PDF, images...) classified into numbered domain folders `01-*` … `11-*` |
| `confluence-pages/` | Curated Markdown, the local source of truth for pages synchronized to Confluence |
| `pm-area/` | Internal Markdown (tracking, analysis, emails, `source-map.md`) that is never published |

New or unclassified files are dropped into `uncategorized/`, which acts as the inbox.

## Install

Copy this directory into:

```text
.claude/skills/confluence-project-assistant/
```

The skill expects a connected Atlassian/Confluence MCP for remote synchronization. It discovers the actual MCP tools at runtime instead of hard-coding provider-specific tool names. Without the MCP, the skill still works locally and reports that Confluence sync was skipped.

## Use cases

The prompts below are examples; phrase them in your own words.

### 1. Start a new project from scratch

You have nothing yet and want a clean workspace to collect documents into.

```text
Initialize a new project documentation workspace for "Project X" in ./project-x.
The content language is Vietnamese.
```

What happens:

- Creates the project root with `README.md`, `project.yaml`, and the system folders `uncategorized/`, `source-documents/`, `confluence-pages/`, `pm-area/`.
- Asks you to confirm the project language if you did not state it, then records it in `project.yaml`.
- Does **not** pre-create `01-*` … `11-*` or any other nested folders; they are created only when a real document belongs there.

Next step: drop your first documents into `uncategorized/` and continue with use case 2.

### 2. Init a project from many unclassified sources

You already have a pile of documents (requirements, architecture decks, meeting notes, emails...) with no structure.

1. Put everything into `uncategorized/` (including `.eml` email threads).
2. Ask:

```text
New documents are available. Process uncategorized.
```

What happens:

- Reads every file, picks the best domain folder and subfolder, and moves each file into `source-documents/` unchanged (original format and filename preserved).
- Registers every moved file in `pm-area/source-map.md`.
- Consolidates facts from many sources into topic pages under `confluence-pages/` (for example `solution-architecture.md`, `functional-requirements.md`); internal analysis goes to `pm-area/`.
- Converts email threads to Markdown in `pm-area/emails/` and extracts their attachments, classifying the real project documents.
- Flags conflicting information between documents instead of silently overwriting it.
- Leaves genuinely ambiguous files in `uncategorized/` and tells you why.
- Syncs only the affected `confluence-pages` to Confluence, if the Atlassian MCP is connected.

### 3. Init a project from existing Confluence pages

You already have a Confluence space or page tree and want a local, versioned, Markdown copy to maintain from now on.

```text
Initialize a project workspace from the Confluence space "PROJ" (parent page "Project X").
Pull the existing pages into confluence-pages/ and keep the page hierarchy.
```

Expected behavior:

- Initializes the workspace as in use case 1, then reads the pages through the Atlassian MCP.
- Writes each page as Markdown under `confluence-pages/`, keeping the parent-child hierarchy and storing the real `page_id`, `space_key` and `parent_page_id` in the front matter, so later syncs update the existing pages instead of creating duplicates.
- Pages that contain internal-only material (tracking, risks, working notes) belong in `pm-area/`, not `confluence-pages/`; the skill asks when it is unclear.
- Page attachments that are project documents can be placed in `uncategorized/` and then processed as in use case 2.
- Requires the Atlassian MCP to be connected. If it is not, nothing is pulled and you are told so.

### 4. Add new documents to a running project

New versions or new documents arrive over time.

```text
New documents are available.
```

- Newly classified files are added to `source-map.md`.
- Existing pages are updated in place (no `architecture-v2.md` duplicates) and only the affected Confluence pages are synced.
- A newer version of an existing file replaces it only when you explicitly say so; otherwise the skill asks.

### 5. Process an email thread with attachments

Drop an `.eml` file into `uncategorized/` and ask to process it.

- The thread becomes a readable Markdown file in `pm-area/emails/` and is never published to Confluence.
- Attachments are extracted and classified into `source-documents/`; unsuitable ones are listed and never deleted without your confirmation.
- Confirmed facts from the thread can update the relevant pages. A thread that looks like an official approval is kept in `pm-area/emails/` until you confirm moving it to `source-documents/`.

### 6. Synchronize with Confluence only

Local Markdown was edited by hand and you only want to push it.

```text
Sync the changed pages in confluence-pages to Confluence.
```

- Updates the mapped Confluence pages and creates a page only when none exists.
- Never publishes `pm-area/` content.
- Reports a page as created/updated only if the MCP operation actually succeeded.

### 7. Adopt an existing documentation folder

You already have a documents folder with its own layout.

```text
Adopt this existing project folder. Do not reorganize my files.
```

- Inspects the current structure first and reuses existing folders and pages.
- Backfills `source-map.md` with the current date for existing files.
- Migrates an older layout (`01-*` … `11-*` in the project root) into `source-documents/` only when you ask.

### 8. Change the project language

```text
Switch the project language to English.
```

- Updates `project.language` in `project.yaml` and asks whether to translate existing pages now.
- Technical, software and project-management terms (sprint, deploy, UAT, risk...) stay in English regardless of the project language.

## Output

After each run the skill reports what was processed, how files were classified, which Markdown pages were created or updated, conflicts needing review, and the Confluence created/updated/skipped counts.
