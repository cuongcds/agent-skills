# Project Structure Reference

## Root layout

| Folder / file | Purpose |
|---|---|
| `uncategorized` | New/unclassified source-document inbox |
| `source-documents` | Original source documents, organized by the numbered domain folders below |
| `confluence-pages` | Curated Markdown intended for Confluence |
| `pm-area` | Internal Markdown not intended for Confluence; includes `source-map.md` and `emails/` (email threads converted to readable `.md`, stored there by default instead of `source-documents/`) |

## Domain folders (inside `source-documents/`)

| Folder | Purpose |
|---|---|
| `01-project-management` | Project governance, planning, meetings, status, risks, issues, decisions |
| `02-business` | Business context, business case, processes and policies |
| `03-requirements` | Functional/non-functional requirements and acceptance criteria |
| `04-architecture` | Solution, application, cloud, infrastructure, network, security and integration architecture |
| `05-design` | Detailed application/API/database/integration/UI/data design |
| `06-development` | Development and repository-related documentation |
| `07-infrastructure` | Infrastructure, environment, compute, network, database, storage, monitoring |
| `08-testing` | Test strategy, plans, cases, results and specialist testing |
| `09-deployment` | Release, deployment, rollback, migration/cutover |
| `10-operation` | Operations, monitoring, backup, DR, incidents, troubleshooting |
| `11-handover` | Application/infrastructure/operations handover and checklists |

## Source path convention

Reference source documents by their path relative to `source-documents/`, without the `source-documents/` prefix (for example `04-architecture/solution/Architecture.pptx`). This applies to page `sources`, traceability notes, conflict records, `source-map.md` and reports.

## Project language

`project.yaml` → `project.language` sets the language of all Markdown in `confluence-pages/` and `pm-area/` (not email conversions or source documents). Confirm with the user at initialization if unknown. Technical, project-management and software-development terms stay in English (sprint, backlog, deploy, milestone, API...).

## Lazy creation

The taxonomy is conceptual. Do not create every folder during initialization. Create only folders needed by actual content.
