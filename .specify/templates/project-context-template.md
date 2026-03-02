# Project Context: [PROJECT_NAME]

**Last Updated**: [DATE]
**Updated By**: Feature [BRANCH_NAME]

## Project Identity

- **Name**: [Project name from repo]
- **Type**: [library|web-app|cli-tool|mobile-app|monorepo]
- **Purpose**: [Brief description of what this project does]
- **Domain**: [Business domain, e.g., e-commerce, analytics, etc.]

## Technology Stack

### Languages & Versions
- [Language]: [Version] (added by [feature-branch])

### Frameworks & Libraries
- [Framework]: [Version] (added by [feature-branch])

### Storage
- [Database/Storage]: [Version] (added by [feature-branch])

### Testing
- [Test Framework]: [Version] (added by [feature-branch])

## Project Structure

```
[Actual directory structure discovered from repository]
```

## API Surface

| Method | Path | Purpose |
|--------|------|---------|
| [GET/POST/...] | [/path] | [One-line description] |

## Runtime Dependency Graph

```
[Process A :port] → [Process B :port] → [External Service]
```

- [Process]: [What it does, what port, how to start it]

## Local Dev Runbook

1. [First command — e.g., install dependencies]
2. [Second command — e.g., start background service]
3. [Third command — e.g., start main server]
4. [Open URL — e.g., http://localhost:8080]

## Data Model Overview

### Entities (Cross-Feature)
- **[Entity Name]** (defined in feature-XXX):
  - Purpose: [What it represents]
  - Key fields: [field (type), field (type), ...]
  - Relationships: [Links to other entities]
  - Special features: [vector columns, indexes, etc.]

### Tool Definitions
- **[Tool Name]**: [target table] — [operation type: SELECT/INSERT/UPDATE/DELETE]

## Domain Glossary

| Term | Definition |
|------|-----------|
| [Term] | [One-line definition] |

## External Integrations

- **[Service Name]**: [Purpose] (added by [feature-branch])
  - Authentication: [Method]
  - Endpoints: [Key endpoints or contracts file]

## Development Workflow

- **Branch Strategy**: Feature branches numbered `###-feature-name`
- **Commit Convention**: [Document if established]
- **Build Command**: [Document from package.json or build config]
- **Test Command**: [Document from package.json or test config]
- **Lint Command**: [Document from package.json or lint config]

## Architecture Patterns

- **Code Organization**: [MVC|Clean Architecture|Feature-based|etc.]
- **Error Handling**: [Document established patterns]
- **State Management**: [Document if applicable]
- **Naming Conventions**: [Document file/class/function naming]

## Recent Features

- [feature-branch]: Added [technology/capability summary]
- [feature-branch]: Added [technology/capability summary]
- [feature-branch]: Added [technology/capability summary]

## Configuration

- **Config Files**: [List key configuration file locations]

### Environment Variable Dependency Chain

| Variable | Consumed By | What Breaks If Missing |
|----------|-------------|----------------------|
| [VAR_NAME] | [component/file] | [consequence] |

## Known Constraints

- [Document any known limitations, technical debt, or workarounds]

<!-- MANUAL ADDITIONS START -->
<!-- Add any manual context below this line -->
<!-- MANUAL ADDITIONS END -->
