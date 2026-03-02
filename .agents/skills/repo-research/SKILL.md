# TODO(codelab): Add YAML frontmatter above this line to activate the skill.
# Antigravity requires ---/name/description/--- to recognize a skill file.

# Repository Research Skill

## Task
Analyze this repository and create or update the project context at `.agents/rules/project-context.md`.

## Critical Rule: Incremental Research Only
DO NOT read all files at once. Follow the phased approach below strictly.
Each phase produces findings that determine WHAT to read next. Never
skip ahead or bulk-read files speculatively.

## Phase 1: Surface Scan (structure only — read NO source files)

1. Run a directory tree command to get the full repo structure:
   ```bash
   find . -not -path './.git/*' -not -path './node_modules/*' \
     -not -path './.venv/*' -not -path './__pycache__/*' | head -200
   ```
2. Record the output as the **Repo Map** — a mental model of directories
   and file names.
3. From the Repo Map alone, identify:
   - **Root config files**: package.json, pyproject.toml, go.mod, etc.
   - **Entry points**: main.py, index.ts, server.py, app.py, cmd/, etc.
   - **Documentation**: README.md, docs/, CONTRIBUTING.md
   - **Infrastructure**: Dockerfile, docker-compose.yaml, .env.example,
     tools.yaml
   - **Data & schema files**: models/, schemas/, migrations/,
     seed_db.py, *.sql, tools.yaml (tool/entity definitions),
     ORM model files (models.py, entities/)
   - **Test directories**: tests/, __tests__/, spec/
4. Write the Repo Map to `.agents/rules/project-context.md` under
   **Project Structure** immediately. If the file does not exist, copy
   the template from `.specify/templates/project-context-template.md`
   first.

**STOP.** Do NOT proceed to Phase 2 until the Repo Map is written to
disk.

## Phase 2: Config & Metadata (read only config files)

Read ONLY the root config and metadata files identified in Phase 1.
Typical files:
- pyproject.toml / package.json / go.mod (dependencies, versions,
  scripts)
- .env.example (required environment variables)
- tools.yaml / docker-compose.yaml (infrastructure dependencies)
- README.md (project description, setup instructions)

From these files, extract and write to project-context.md:
- **Project Identity** (name, type, purpose, domain)
- **Technology Stack** (languages, frameworks, versions)
- **Configuration** (environment variables, config file locations)
- **Development Workflow** (build/test/lint commands)

**STOP.** Do NOT read source code files yet.

## Phase 3: Entry Points & Data Model (read entry points + schema files)

Read the entry point files identified in Phase 1 (e.g., server.py,
agent.py, __init__.py, main.py) AND any data/schema files identified
in Phase 1 (e.g., seed_db.py, migrations/, models.py, tools.yaml
tool definitions).

Limit to TOP-LEVEL entry points — do NOT follow imports into
submodules yet.

From entry points, extract:
- **Architecture Patterns** (MVC, agent framework, microservices, etc.)
- **External Integrations** (API clients, database connections,
  third-party services)
- **API Surface / Route Map** — list every HTTP endpoint, WebSocket,
  or SSE route exposed by the application. For each route, document:
  method, path, and one-line purpose
  (e.g., `POST /run_sse — SSE stream of agent responses`)
- **Runtime Dependency Graph** — document the process chain required
  at runtime. Which processes must be running, what ports they bind,
  and the call direction between them. Example:
  `Browser → uvicorn :8080 → ADK Agent → Toolbox :5000 → Cloud SQL`
- **Local Dev Runbook** — extract the exact sequence of commands
  needed to start the application locally (install deps, start
  background services, start main server, open URL). If spread
  across README + scripts, consolidate into a single ordered list
- **Environment Variable Dependency Chain** — for each env var,
  document which component consumes it and what breaks if it is
  missing (e.g., `DB_PASSWORD → used by seed_db.py and tools.yaml
  Cloud SQL connector; missing = connection refused`)
- **Domain Glossary** — identify project-specific or framework-
  specific terms that appear in the code and would be unfamiliar to
  a new engineer. For each term, write a one-line definition
  (e.g., `ToolContext: ADK object that provides read/write access
  to session state within a tool function`)

From data/schema files, extract:
- **Data Model Overview** — for each entity/table found, document:
  - Entity name and purpose
  - Key fields/columns and types
  - Relationships to other entities (foreign keys, references)
  - Special features (vector columns, generated columns, indexes)
- **Tool definitions** — if tools.yaml or similar defines database
  tools, document each tool's name, target table, and operation type
  (SELECT, INSERT, UPDATE, DELETE)

Write findings to the corresponding sections in project-context.md.

## Phase 4: Targeted Deep Dive (read specific files on demand)

Only if a section in project-context.md still has placeholder tokens
`[...]` after Phases 1-3, identify the SPECIFIC file that would resolve
the placeholder and read ONLY that file.

Rules:
- Read ONE file at a time, extract what you need, then decide if another
  file is required.
- Maximum of 5 additional files in this phase.
- If a section cannot be resolved within 5 files, leave it with
  placeholder tokens and add a comment:
  `<!-- TODO: Could not determine from available files -->`

## Incremental Update Rules
- NEVER silently overwrite existing completed sections.
- APPEND new technologies, entities, or integrations to existing lists.
- UPDATE the "Last Updated" date and "Updated By" field.
- Write to disk at the end of EACH phase, not just at the end. If
  interrupted, all progress from completed phases is preserved —
  re-invoking the skill picks up from where it left off.

## Conflict Resolution
If your research findings contradict what is already documented in
project-context.md:
- DO NOT silently overwrite the existing content.
- REPORT each inconsistency to the user in this format:
  **Inconsistency found in [Section Name]:**
  - Documented: [what project-context.md currently says]
  - Actual: [what the repository research found]
  - Suggestion: [recommended update]
- WAIT for the user to confirm before making changes to conflicting
  sections.
- If the user does not respond or the session ends, leave the existing
  content unchanged and add a comment:
  `<!-- REVIEW: [brief description of inconsistency] -->`.
