# Agent Skills

A collection of agent skills from my day-to-day work, published on [skills.sh](https://www.skills.sh).

## Install

Requires [Node.js](https://nodejs.org) (for `npx`).

Install all skills from this repository:

```bash
npx skills add cuongcds/agent-skills
```

Install a specific skill:

```bash
npx skills add cuongcds/agent-skills --skill confluence-project-assistant
```

List the skills available in this repository without installing:

```bash
npx skills add cuongcds/agent-skills --list
```

Or use the full repository URL:

```bash
npx skills add https://github.com/cuongcds/agent-skills
```

The CLI will prompt you to choose the target agent(s) (Claude Code, Cursor, Codex, ...) and whether to install per project or globally.

## Skills

| Skill                                                                 | Category      | Description                                                                                                                                                                      |
| --------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [confluence-project-assistant](pm-agents/confluence-project-assistant) | `pm-agents` | Initialize and maintain a project documentation workspace: classify source documents, normalize them into Markdown, and sync eligible pages to Confluence via the Atlassian MCP. |

### confluence-project-assistant

**Requirements**

- An Atlassian MCP server connected to your agent (only needed for the Confluence sync step).
- Python 3 (for the helper script `scripts/eml_to_md.py`).

**Use it when you want to**

- Create a project documentation workspace.
- Process new project documents dropped into `uncategorized/`.
- Update project documentation.
- Synchronize project knowledge with Confluence.

See the skill's own [README](pm-agents/confluence-project-assistant/README.md) and [SKILL.md](pm-agents/confluence-project-assistant/SKILL.md) for details.

## Repository layout

```
agent-skills/
└── pm-agents/
    └── confluence-project-assistant/
        ├── SKILL.md
        ├── README.md
        ├── references/
        ├── scripts/
        └── templates/
```

Each skill lives in its own folder, grouped by category, and is defined by a `SKILL.md` file.

## Manual install

If you prefer not to use the CLI, clone the repo and copy a skill folder into your agent's skills directory:

```bash
git clone https://github.com/cuongcds/agent-skills.git

# Claude Code, global
cp -r agent-skills/pm-agents/confluence-project-assistant ~/.claude/skills/

# Claude Code, current project only
cp -r agent-skills/pm-agents/confluence-project-assistant .claude/skills/
```

## Adding more skills

New skills will be added over time. Check back here or run `npx skills add cuongcds/agent-skills --list` to see what is available.
