# Tasks: Cloud Run Deployment Pipeline & Secure Containerization

**Input**: Design documents from `/specs/002-cloudrun-deploy-pipeline/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: All new endpoints must have tests written before implementation (Shift-Left Testing with pytest).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `Dockerfile`, `cloudbuild.yaml` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize container ignore patterns in `.dockerignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Implement minimal python:3.11-slim base runtime configuration in `Dockerfile`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Containerized Local Execution (Priority: P1) 🎯 MVP

**Goal**: Package the primary application as a standalone container image capable of running predictably locally or in any cloud environment.

**Independent Test**: Fully verifiable by running docker build locally and checking non-root startup on exposed port 8080.

### Implementation for User Story 1

- [x] T003 [P] [US1] Configure non-root user appuser (UID 10001) runtime context in `Dockerfile`
- [x] T004 [US1] Expose web server port 8080 and define Uvicorn live entrypoint in `Dockerfile`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Automated Cloud Deployment Trigger (Priority: P2)

**Goal**: Configure continuous integration and delivery (CI/CD) triggering automated container registry push and Cloud Run rollout upon git commits to main.

**Independent Test**: Verifiable by validating build pipeline syntax and local runner emulation.

### Implementation for User Story 2

- [x] T005 [US2] Define image build, container push, and Cloud Run deploy rollout steps in `cloudbuild.yaml`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Credential Injection (Priority: P3)

**Goal**: Inject runtime database connection secrets dynamically from Google Secret Manager.

**Independent Test**: Verifiable via Cloud Run secret binding parameter verification and confirming zero plain-text credential leaks in image layers.

### Implementation for User Story 3

- [x] T006 [US3] Bind database connection secrets (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) using Secret Manager flag in `cloudbuild.yaml`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T007 [P] Update local container runbook and deployment instructions in `README.md`
- [x] T008 Run docker build verification locally to prove zero build warnings and size compliance (<250MB) in `Dockerfile`
- [x] T009 Verify quickstart.md local execution commands in `specs/002-cloudrun-deploy-pipeline/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on container build definition (US1)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates into US2 pipeline rollout

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch container base directives and user configuration together:
Task: "Configure non-root user appuser (UID 10001) runtime context in Dockerfile"
Task: "Expose web server port 8080 and define Uvicorn live entrypoint in Dockerfile"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories
