# Tasks: Table Reservation System

**Input**: Design documents from `/specs/001-table-reservation-api/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: All new endpoints must have tests written before implementation (Shift-Left Testing with pytest).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `restaurant_concierge/`, `tests/` at repository root
- Paths shown below assume single project structure as per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

 [x] T001 Setup test configuration and folder structure in `tests/conftest.py`


## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

 [x] T002 Create database connection and session management in `restaurant_concierge/database.py`
 [x] T003 [P] Implement base database model and SQLAlchemy schema setup in `restaurant_concierge/models.py`
 [x] T004 [P] Configure environment variables and pre-shared API key check in `restaurant_concierge/reservations.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Table Reservation (Priority: P1) 🎯 MVP

**Goal**: Allow customers to submit reservation requests and validate them.

**Independent Test**: Submit a booking request for an available slot and verify that a confirmation is received.

### Tests for User Story 1 (MANDATORY for new endpoints per Constitution) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

 [x] T005 [P] [US1] Create validation tests for reservation inputs (valid reservation, past dates, invalid party sizes) in `tests/test_reservations.py`

### Implementation for User Story 1

 [x] T006 [P] [US1] Define SQLAlchemy model `Reservation` and Pydantic schema `ReservationCreate` in `restaurant_concierge/models.py`
 [x] T007 [US1] Implement reservation creation service logic with input validation in `restaurant_concierge/reservations.py`
 [x] T008 [US1] Define POST `/reservations` API endpoint and register it to the FastAPI app in `server.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Prevent Overbooking (Priority: P2)

**Goal**: Reject reservations that exceed the restaurant's seating capacity (static 40 seats) for a given slot.

**Independent Test**: Fill all available capacity for a specific time slot, attempt to book one additional guest, and verify that the system rejects the booking.

### Tests for User Story 2 (MANDATORY for new endpoints per Constitution) ⚠️

 [x] T009 [P] [US2] Create overbooking capacity tests and concurrent double-booking prevention tests in `tests/test_reservations.py`

### Implementation for User Story 2

 [x] T010 [US2] Implement capacity check logic using row-level locking (`SELECT ... FOR UPDATE`) in `restaurant_concierge/reservations.py`
 [x] T011 [US2] Integrate capacity check into the POST `/reservations` endpoint in `restaurant_concierge/reservations.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - List Reservations (Priority: P3)

**Goal**: Retrieve the complete list of reservations using API key authentication.

**Independent Test**: Retrieve the list with correct API key, verify retrieval, and verify unauthorized code (401) on missing/invalid key.

### Tests for User Story 3 (MANDATORY for new endpoints per Constitution) ⚠️

 [x] T012 [P] [US3] Create list retrieval security and logic tests (valid key, invalid key, missing key) in `tests/test_reservations.py`

### Implementation for User Story 3

 [x] T013 [US3] Implement API key authentication dependency using FastAPI's `Security` and `APIKeyHeader` in `restaurant_concierge/reservations.py`
 [x] T014 [US3] Define GET `/reservations` endpoint secured with API key dependency in `restaurant_concierge/reservations.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T015 [P] Update local configuration / runtime runbook in `README.md`
- [x] T016 Run all tests via pytest to verify 100% test coverage and compliance with success criteria
- [x] T017 Run quickstart.md validation script / verification manually

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all models/schemas for User Story 1 together:
Task: "Define SQLAlchemy model Reservation and Pydantic schema ReservationCreate in restaurant_concierge/models.py"
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
