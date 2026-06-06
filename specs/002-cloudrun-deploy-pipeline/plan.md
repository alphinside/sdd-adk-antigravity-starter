# Implementation Plan: Cloud Run Deployment Pipeline & Secure Containerization

**Branch**: `002-cloudrun-deploy-pipeline` | **Date**: 2026-06-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-cloudrun-deploy-pipeline/spec.md`

## Summary

Containerize the FastAPI application using a minimal, hardened `python:3.11-slim` Dockerfile running under an unprivileged non-root user (`appuser` UID 10001). Implement a fully automated Google Cloud Build CI/CD pipeline (`cloudbuild.yaml`) triggered on pushes to the `main` branch, deploying directly to Google Cloud Run while dynamically binding sensitive database connection parameters (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`) from Google Secret Manager.

## Technical Context

**Language/Version**: Python 3.11 (`python:3.11-slim` runtime)  
**Primary Dependencies**: Docker, Google Cloud SDK (`gcloud run deploy`), Google Secret Manager  
**Storage**: Cloud SQL (PostgreSQL)  
**Testing**: Container verification via `docker build` and local port binding check  
**Target Platform**: Google Cloud Run (Serverless Container Platform)  
**Project Type**: Standalone Web Application Container  
**Performance Goals**: Container startup under 5 seconds  
**Constraints**: Zero hardcoded plaintext database secrets within container layers  
**Scale/Scope**: Automated CI/CD deployment triggered on commit pushes to `main`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Unified Tech Stack**: Does this service use FastAPI for web services and Cloud SQL (PostgreSQL) for the database?
- [x] **Shift-Left Testing**: Are tests written using pytest *before* implementation for all new endpoints?
- [x] **BDD Specifications**: Does the feature specification follow Behavior-Driven Development (BDD) principles (Given/When/Then)?

## Project Structure

### Documentation (this feature)

```text
specs/002-cloudrun-deploy-pipeline/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── openapi.json
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
/Users/gumoreira/sdd-adk-antigravity-starter/
├── Dockerfile           # Minimal python:3.11-slim non-root runtime container definition
├── .dockerignore        # Excludes virtual environments (.venv), temp caches, git metadata
└── cloudbuild.yaml      # Cloud Build CI/CD workflow coordinating image compile and Cloud Run deployment
```

**Structure Decision**: Standalone single project container rollout configuration situated at repository root.

## Complexity Tracking

*(No architectural violations. Architecture fully adheres to cloud-native serverless security and minimal Docker container standards.)*
