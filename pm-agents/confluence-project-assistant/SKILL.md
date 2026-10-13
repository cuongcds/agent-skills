---
name: confluence-project-assistant
description: Initialize and maintain a project documentation workspace. Classify newly provided source documents from uncategorized, preserve original files under source-documents in the appropriate numbered domain folders, track them in pm-area/source-map.md, normalize project knowledge into Markdown under confluence-pages and pm-area, and synchronize eligible confluence-pages Markdown to Confluence through the connected Atlassian MCP. Use when creating a project workspace, processing new project documents, updating project documentation, or synchronizing project knowledge with Confluence.
---

# Confluence Project Assistant
## Purpose

This skill manages a project documentation workspace across three layers:

1. **`source-documents/`** — original DOCX, XLSX/XLS, PPTX/PPT, PDF, image and other supported project files, organized under the appropriate numbered domain folder (`01-*` … `11-*`).
2. **`confluence-pages/`** — normalized, curated Markdown that represents project knowledge intended for publication to Confluence.
3. **`pm-area/`** — normalized Markdown for internal project-management, analysis, working notes, tracking and other information that must not be published to Confluence. It also holds `source-map.md`, the register of everything in `source-documents/`.

`uncategorized/` (project root) is the inbox for new/unclassified documents. It is not part of `source-documents/`; classified files move from the inbox into `source-documents/`, and files left in the inbox are not listed in `source-map.md`.

### Source path convention

Whenever a source document is referenced (front matter `sources`, traceability notes, `source-map.md`, conflict records, reports), use its path **relative to `source-documents/`** and never include the `source-documents/` prefix. Example: `04-architecture/solution/Architecture.pptx`, not `source-documents/04-architecture/solution/Architecture.pptx`.

## Core Principles

- Preserve original source files. Never replace a source file with Markdown.
- Never create empty project folders. All folders except the system folders are created on demand only when a real document or Markdown artifact belongs there.
- Do not create Markdown files merely because a category exists. Create/update a Markdown file only when there is substantive information for it.
- Treat `confluence-pages/*.md` as the local source of truth for content that is synchronized to Confluence.
- Do not publish `pm-area` content to Confluence.
- A source document is evidence/input, not automatically a one-to-one Confluence page.
- Consolidate related information from multiple source documents into the appropriate Markdown knowledge page.
- When new information changes existing knowledge, update the existing Markdown page instead of creating a versioned duplicate such as `architecture-v2.md`.
- Do not silently overwrite conflicting information. Identify conflicts and preserve traceability to the relevant source documents.
- Do not invent facts that are not supported by project documents or explicit user instructions.
- Prefer the latest authoritative project source when recency and authority are clear; otherwise flag the conflict for review.
- Keep the source file's original format and filename unless there is a clear need to rename/move it. Do not modify source content as part of classification.

## Project Language

The project has a content language, stored in `project.yaml` as `project.language` (a short code such as `vi` or `en`).

- **Scope:** every Markdown file written under `confluence-pages/` and `pm-area/` (prose, headings, table text, notes) uses this language. Not affected: source documents, file/folder names, front matter keys, `source-map.md` structure, and email threads converted to `pm-area/emails/` (their wording is preserved as-is).
- **Resolve it before writing any page:**
  1. Read `project.language`. If set, use it.
  2. If empty, do not guess silently. Ask the user which language to use, offering a suggestion inferred from the source documents or the conversation, then save the answer to `project.yaml`.
  3. Headless/no-user runs: do not ask. Infer from the dominant language of existing pages (else the source documents), write it to `project.yaml`, and flag it in the report for confirmation.
- **Changing language:** if the user changes `project.language`, update `project.yaml` and ask whether to translate existing pages now; do not rewrite them unasked. Until translated, new/updated pages use the new language.
- **Keep technical terms in the original English.** Do not translate terms from software development, IT infrastructure/cloud, or project management/delivery (for example: sprint, backlog, milestone, stakeholder, deadline, deploy, release, rollback, cutover, pipeline, repository, branch, API, endpoint, requirement, user story, UAT, risk, issue, dependency, roadmap, status report, workstream, wave). Write them as-is inside sentences of the project language, e.g. "Hoàn thành sprint 3 trước milestone UAT", not a forced translation. Likewise keep product names, tool names, proper nouns, acronyms and identifiers (ticket keys, hostnames, code) untouched.
- Section headings from templates are written in the project language, but heading words that are technical terms stay in English.
- The Output Report to the user follows the language of the conversation, not necessarily the project language.

## Workspace Structure

The logical project structure is:

```text
<project-root>/
├── README.md
├── project.yaml
├── uncategorized/
├── source-documents/
│   ├── 01-project-management/
│   ├── 02-business/
│   ├── 03-requirements/
│   ├── 04-architecture/
│   ├── 05-design/
│   ├── 06-development/
│   ├── 07-infrastructure/
│   ├── 08-testing/
│   ├── 09-deployment/
│   ├── 10-operation/
│   └── 11-handover/
├── confluence-pages/
└── pm-area/
    └── source-map.md
```

This is a logical taxonomy, not a requirement to create all folders.

### On-demand folder rule

Do **not** pre-create `01-*` through `11-*`, their nested folders, or nested folders inside `confluence-pages/` and `pm-area/`. The `01-*` … `11-*` folders live only inside `source-documents/`, never in the project root.

Example: if the first source is an architecture presentation, create only what is required:

```text
source-documents/
└── 04-architecture/
    └── solution/
        └── Architecture.pptx
```

Do not create unrelated folders such as `07-infrastructure/`, `08-testing/`, etc.

`uncategorized/`, `source-documents/`, `confluence-pages/`, and `pm-area/` are system areas. They may be created during project initialization, or lazily when first needed; do not create additional nested folders inside them until needed.

## Source Document Taxonomy

Use the following taxonomy as the default classification model. All folders below are created inside `source-documents/`. Adapt the nested folder name to the actual document content and project context.

### 01-project-management
Project governance and delivery management material:

- project charter / project overview
- project plan and schedule
- milestones
- meeting minutes
- status reports
- action items
- risks and issues
- dependencies
- decisions
- correspondence

Example:

```text
01-project-management/
├── plan/
├── meeting/
├── status-report/
├── risk/
├── issue/
├── dependency/
└── decision/
```

Create only the needed subfolders.

### 02-business
Business context and business-facing material:

- business case
- business requirements
- business process
- policy
- business model
- operating model

### 03-requirements
System/product requirements:

- functional requirements
- non-functional requirements
- use cases
- user stories
- acceptance criteria
- requirements specifications

### 04-architecture
Architecture and solution design at the architectural level:

- solution architecture
- application architecture
- infrastructure architecture
- cloud architecture
- network architecture
- security architecture
- integration architecture
- data architecture
- architecture decisions

### 05-design
Detailed design:

- application design
- API design
- database design
- integration design
- UI/UX design
- data model

### 06-development
Development implementation material:

- repository information
- development guide
- coding standards
- source-code related documents
- development configuration

### 07-infrastructure
Infrastructure/platform material:

- environments
- compute
- network
- database
- storage
- security
- monitoring
- cloud resource specifications

### 08-testing
Testing material:

- test strategy
- test plan
- test cases
- test results
- performance testing
- security testing
- UAT

### 09-deployment
Release and deployment:

- deployment plan
- release plan
- rollback plan
- deployment checklist
- migration/cutover plan

### 10-operation
Post-deployment operations:

- operations guide
- monitoring
- backup/restore
- disaster recovery
- incident management
- troubleshooting
- maintenance

### 11-handover
Delivery/handover material:

- application handover
- infrastructure handover
- operations handover
- handover checklist
- knowledge transfer

## `uncategorized` Workflow

When the user says that new documents are available, interpret that as: **scan and process the files currently located in `uncategorized/`**.

Workflow:

1. List all supported files in `uncategorized/`.
2. Ignore generated/intermediate files that are clearly not project source material unless the user asks otherwise.
3. Read every relevant file.
3a. Handle email threads separately (`.eml`, `.msg`, exported mail threads; see "Email threads" below): by default move them to `pm-area/emails/`, not to `source-documents/`, and skip steps 4–9 for them.
4. Determine the best source-domain and subfolder for each remaining file.
5. If a file contains mixed topics, classify it according to its primary purpose and use its contents to update multiple Markdown knowledge pages when necessary.
6. Create only the source folders actually required, inside `source-documents/`.
7. Move each classified source file from `uncategorized/` to its selected folder under `source-documents/` while preserving its original format and filename.
8. If classification is genuinely ambiguous, do not guess. Leave the file in `uncategorized/` and report the ambiguity.
9. Register every moved file in `pm-area/source-map.md` (see `pm-area/` Rules).
10. Analyze each document against existing project knowledge before writing Markdown.
11. Create or update relevant files under `confluence-pages/` and `pm-area/`, written in the project language (see "Project Language"; keep technical/PM/software terms in English).
12. Detect new facts, changed facts, superseded facts, removals, assumptions, open questions, risks, dependencies and decisions.
13. Synchronize only the affected `confluence-pages` content to Confluence using the connected Atlassian MCP.
14. Report what was classified, what Markdown was created/updated, what conflicts were found, and what Confluence pages were created/updated.

After successful classification, `uncategorized/` should contain only files that could not yet be confidently classified or explicitly require user review.

### Email threads

Email threads are internal communication, not project source documents.

- Default: convert each email thread file from `uncategorized/` into a readable Markdown file and store it in `pm-area/emails/` (created on demand). Only the `.md` goes into `emails/`, never the raw `.eml`/`.msg`. Do not add it to `source-map.md`, and never publish it to Confluence.
- Conversion: use `scripts/eml_to_md.py <input.eml> pm-area/emails uncategorized/attachments` for `.eml` (output name `<YYYY-MM-DD>-<subject-slug>.md`; the date is the date of the latest message). For `.msg` or other formats, produce the same layout by hand. The `.md` must be human-readable: a title (subject without `Re:`/`Fwd:` prefixes), a From/To/Cc/Date/Subject/Original file table, an Attachments list (names and sizes, excluding inline images and signature graphics) and the cleaned message text with its quoted history. Drop signature graphics and tracking noise; do not summarize or alter the wording.
- Attachments: before the original email is removed, every attachment is extracted to `uncategorized/attachments/<email-md-name>/` (all documents and explicit attachments; inline images only when meaningful, i.e. ≥100 KB — look at them to decide; tiny signature/logo graphics are skipped and counted in the `.md`). The `.md` lists each extracted file. Then handle each extracted file:
  1. If it is a project document that fits the taxonomy, classify it like any other file: move it from `uncategorized/attachments/` to the matching folder under `source-documents/`, register it in `source-map.md`, and use it as input for the pages. If a file of the same name exists there, follow the replace/ask rule of `source-map.md`.
  2. If it is not suitable (duplicate, irrelevant image, signature graphic, unreadable), do not delete it on your own: list it and ask the user to confirm before deleting.
  3. If classification is unclear, leave it in `uncategorized/attachments/` and report it.
  4. If an attachment is an older/superseded version of a document already in `source-documents/`, it is still a project document: ask the user whether to keep it (under a different filename, never overwriting) or delete it.
  After placing each file, update the Attachments list in the email's `.md` so it shows the final location (path relative to `source-documents/`) instead of the temporary `uncategorized/attachments/` path. Give a file a descriptive name when its original name is meaningless (for example `image020.png`), and say so in the report.
- Only after the `.md` is written and checked to be readable and all attachments are extracted, delete the original email file from `uncategorized/`. Remove an empty `uncategorized/attachments/<email-md-name>/` folder once its files are placed or deleted.
- Read the thread and use it like any other input: update `pm-area` tracking pages and, when it carries confirmed official project facts, the relevant `confluence-pages`. Cite the thread as `emails/<filename>.md` (relative to `pm-area/`).
- Special case: if a thread (or its attachment) looks like an official source document — for example a signed approval, a formal decision or a contractual confirmation that should be kept as evidence — do not decide alone. Ask the user to confirm first. Only after explicit confirmation, move it into the matching domain folder under `source-documents/` and register it in `source-map.md`; until then leave it in `pm-area/emails/`.
- Attachments are never discarded silently; see "Attachments" above.
- In headless/no-user runs, do not ask: store the converted `.md` in `pm-area/emails/`, keep attachments in `uncategorized/attachments/` (classify only the clear-cut ones, never delete), and list the special cases and unconfirmed deletions in the report.

## Document-to-Knowledge Processing

Do not use a one-source-file-to-one-Markdown-file mapping.

Instead:

```text
Source documents
      ↓
Read + extract
      ↓
Classify + compare with existing knowledge
      ↓
 ┌───────────────┬──────────────────┐
 │               │                  │
 ▼               ▼                  ▼
New facts    Changed facts      Internal analysis
 │               │                  │
 └───────┬───────┘                  │
         ▼                          ▼
confluence-pages/               pm-area/
```

A single source document may update multiple Markdown files. Multiple source documents may contribute to one Markdown file.

## `confluence-pages/` Rules

`confluence-pages/` contains only curated Markdown intended to represent official project knowledge.

Suggested logical taxonomy:

```text
confluence-pages/
├── 00-project-overview.md
├── 01-business/
├── 02-requirements/
├── 03-architecture/
├── 04-design/
├── 05-development/
├── 06-infrastructure/
├── 07-testing/
├── 08-deployment/
├── 09-operation/
└── 10-handover/
```

This is not a pre-created structure. Create a folder/page only when information actually exists.

Use stable topic-oriented filenames such as:

- `solution-architecture.md`
- `network-architecture.md`
- `security-architecture.md`
- `functional-requirements.md`
- `deployment-plan.md`

Avoid filenames based solely on source-document versions such as `architecture-v2.md` unless the user explicitly wants document-version pages.

### Markdown page metadata

Each synchronized Markdown page should have front matter when practical:

```yaml
---
title: Solution Architecture
confluence:
  page_id: ""
  space_key: ""
  parent_page_id: ""
status: draft
last_sync: ""
sources:
  - 04-architecture/solution/Architecture.pptx
---
```

Do not invent a Confluence page ID or space key. Populate these values only from actual Confluence state or explicit user configuration.

If a page is not yet synchronized, use empty values or omit fields that cannot be known.

## `pm-area/` Rules

`pm-area/` contains internal Markdown that should **not** be pushed to Confluence.

Typical on-demand content:

```text
pm-area/
├── source-map.md
├── emails/
├── project-status.md
├── project-tracking.md
├── action-items.md
├── risks.md
├── issues.md
├── dependencies.md
├── decisions.md
├── meeting-notes/
├── analysis/
└── working-notes/
```

Again, create only what is needed. `source-map.md` is required as soon as the first document is classified into `source-documents/`.

### `source-map.md`

`pm-area/source-map.md` is the register of all documents in `source-documents/`. It is internal and is never published to Confluence.

Format:

````markdown
# Source Map

Tree of `source-documents/`. Dates are YYYY-MM-DD.

```text
source-documents/
├── 03-requirements/
│   └── functional/
│       └── Requirements.docx  [added: 2026-10-05 | updated: 2026-10-07]
└── 04-architecture/
    └── solution/
        ├── Architecture.pptx  [added: 2026-10-05]
        └── Network.pdf  [added: 2026-10-06]
```
````

Rules:

- Present the map as a folder tree in a single `text` code block, mirroring the actual folders and files under `source-documents/` (only folders that contain files). Sort folders and files alphabetically.
- Each file line ends with `[added: <date>]`. Append `| updated: <date>` only when the update date differs from the added date. The root line is `source-documents/`; building the path of a file from the tree gives the path relative to `source-documents/`, matching the paths used in page `sources`.
- `added` is the date (YYYY-MM-DD) the file was moved into `source-documents/`.
- `updated` is the date the file's content was last replaced by a newer version. Omit it on a file that was never updated, and omit it if the update happened on the same day as `added`.
- When a file is moved or renamed, move or rename its node in the tree and keep `added`.
- When the user supplies a newer version that replaces an existing file, replace it only on explicit instruction, then add or change `updated` to that date (unless it equals `added`). If a file with the same name already exists and replacement was not requested, do not overwrite; ask the user.
- Keep the tree in sync with the folder contents: every file added to or removed from `source-documents/` is reflected in the same operation.
- When adopting an existing project, backfill every existing file with the current date as `added` (no `updated`) unless a reliable date is known.

Use `pm-area` for:

- internal analysis
- gap analysis
- working notes
- PM tracking
- unresolved questions
- internal risks/issues
- meeting notes when they are not intended for publication
- implementation or migration analysis prepared for internal use

If a source document contains both official project facts and internal analysis, split the resulting knowledge appropriately between `confluence-pages` and `pm-area`.

## Conflict and Version Handling

When new material conflicts with existing knowledge:

1. Identify the conflicting statements.
2. Identify their source documents.
3. Determine whether one source is clearly newer or more authoritative.
4. If the newer/authoritative source is clear, update the canonical Markdown and retain a concise note about the previous state when useful.
5. If authority is unclear, do not silently overwrite. Record the conflict in `pm-area` and report it to the user.
6. Never fabricate a resolution.

Example:

```markdown
## Database Platform

The latest approved architecture specifies Oracle as the target database.

### Previous Information

An earlier architecture document specified PostgreSQL.

### Source Traceability

- Latest: `04-architecture/solution/Architecture-v2.pptx`
- Previous: `04-architecture/solution/Architecture-v1.pptx`
```

## Confluence Synchronization

Use the connected Atlassian/Confluence MCP when available.

Before performing a synchronization:

1. Discover the available Atlassian/Confluence MCP tools if their exact names are not already known.
2. Identify the target Confluence space and page hierarchy from project configuration or existing page metadata.
3. For each affected Markdown page, determine whether the corresponding Confluence page already exists.
4. Update an existing page when a mapping exists.
5. Create a page only when no corresponding page exists.
6. Preserve the intended parent-child hierarchy.
7. Never create duplicate Confluence pages simply because a source document changed.
8. Never publish `pm-area` files.
9. Do not claim synchronization succeeded unless the MCP operation actually succeeds.
10. If Atlassian MCP is unavailable or not connected, update local Markdown and report that Confluence synchronization was skipped.

The skill must not assume a particular Atlassian MCP tool name or schema. Discover the connected tools at runtime and follow their actual contracts.

## Initialization Workflow

When asked to initialize a project:

1. Validate the requested project root.
2. Create the project root if it does not exist.
3. Create `README.md` and `project.yaml` if absent.
4. Create the system inbox/work areas as appropriate: `uncategorized/`, `source-documents/`, `confluence-pages/`, `pm-area/`.
5. Do **not** create `01-*` through `11-*` (inside `source-documents/`) or any nested folders unless there is already content that belongs there. Create `pm-area/source-map.md` only when the first source document is classified.
6. Initialize `project.yaml` with project metadata only when known. For `project.language`: if the user already stated the language, use it; if not (or unclear), ask the user to confirm before finishing initialization, then write it. Never leave it silently defaulted.
7. Report the actual folders created and the chosen project language.

## Existing Project Workflow

When working on an existing project:

- Inspect the existing structure before creating anything.
- Check `project.language` in `project.yaml`. If it is missing/empty, resolve it per "Project Language" before writing or updating any page.
- Reuse existing folders and Markdown pages where they match the taxonomy.
- Do not reorganize or rename existing documents merely to match this skill unless the user asks for migration/reorganization.
- Preserve project-specific conventions when they are reasonable and consistent.
- If the project still has the older layout (`01-*` … `11-*` directly in the project root), keep working with it until the user asks to migrate. On migration, move those folders into `source-documents/` unchanged, create or update `pm-area/source-map.md` for all moved files, and leave existing page `sources` paths as they are (they are already relative to the domain folders).

## Traceability

For every meaningful Markdown update, retain source traceability where practical.

A page should be able to answer:

- What source document supplied this information?
- Was the information newly added or updated?
- What assumptions remain?
- What conflicts were detected?

Do not copy large amounts of source text verbatim. Summarize and normalize the information while preserving important technical details, requirements, constraints and decisions.

## Output Report

After processing new documents, report:

```text
Project Documentation Update

Processed:
- <file>

Source classification (paths relative to source-documents/):
- <file> → <domain folder>/<subfolder>

Markdown created/updated:
- confluence-pages/<page>.md
- pm-area/source-map.md
- pm-area/<page>.md

Conflicts / review required:
- <item or None>
- <language assumed, if inferred in a headless run>


Confluence:
- Created: N pages
- Updated: N pages
- Skipped: N pages
```

Only report successful Confluence operations as created/updated.

## Safety / Quality Rules

- Never leave `pm-area/source-map.md` out of sync with `source-documents/`.
- Never delete source documents as part of normal processing.
- Never overwrite a source file with normalized content.
- Never create empty directories for hypothetical future categories.
- Never publish internal PM material by accident.
- Never create duplicate Markdown pages when an existing canonical page can be updated.
- Never create duplicate Confluence pages when an existing page can be updated.
- Never resolve contradictory requirements by guessing.
- Never write pages in `confluence-pages/` or `pm-area/` before the project language is known and recorded in `project.yaml`.
- Never translate technical, project-management or software-development terms; keep the English original.
- Never claim a document was read if it could not actually be accessed.
- Never claim Confluence was synchronized if the Atlassian MCP operation did not succeed.
