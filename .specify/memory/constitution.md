<!--
=== SYNC IMPACT REPORT ===
Version change: 0.0.0 -> 1.0.0
List of modified principles:
  - N/A (Initial ratification of 3 new principles)
Added sections:
  - Core Principles (I. Unified Tech Stack, II. Shift-Left Testing, III. Behavior-Driven Development)
  - Development Quality Standards
  - Workflow & Release Guidelines
Removed sections:
  - N/A (Placeholders replaced)
Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
Follow-up TODOs:
  - None
==========================
-->

# Restaurant Concierge Constitution

## Core Principles

### I. Unified Tech Stack (FastAPI & Cloud SQL)
FastAPI MUST be used for developing all web services. Cloud SQL (PostgreSQL dialect) MUST be used as the central database.

### II. Shift-Left Testing (pytest)
All new endpoints MUST have automated tests written using `pytest` before the implementation begins. Tests must be validated to fail first, then implementation must proceed to make them pass.

### III. Behavior-Driven Development (BDD)
Feature specifications MUST follow Behavior-Driven Development principles (e.g., Given/When/Then style format) to define acceptance criteria and clear user scenarios before implementation begins.

## Development Quality Standards

All code modifications must run clean of lint errors and satisfy existing workspace guidelines. Complexity must be minimized and justified where necessary.

## Workflow & Release Guidelines

Build and test execution commands must be verified locally before pushing to origin. The specify -> plan -> tasks -> implement workflow cycle must be followed.

## Governance

This constitution is the single source of truth for repository structure and quality gates. Amendments to these principles require team consensus, updating this document, and an increment to the constitution version. Compliance must be checked in all feature planning phases.

**Version**: 1.0.0 | **Ratified**: 2026-06-05 | **Last Amended**: 2026-06-05