# Data Model: Cloud Run Deployment Pipeline

## Entities

### `ContainerRuntimeConfig`

Defines the parameters and runtime specifications for the secure Docker container.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `base_image` | `STRING` | `NOT NULL` | Base image reference (`python:3.11-slim`). |
| `user_uid` | `INTEGER` | `DEFAULT 10001` | Non-root system user identifier. |
| `exposed_port` | `INTEGER` | `DEFAULT 8080` | Network port exposed to Cloud Run proxy. |
| `env_vars` | `MAP` | `REQUIRED` | Unbuffered and bytecode prevention tokens. |

### `DeploymentPipelineSchema`

Coordinates the metadata and trigger bindings for Google Cloud Build execution.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `trigger_branch` | `STRING` | `DEFAULT 'main'` | Git reference triggering deployment rollout. |
| `service_name` | `STRING` | `DEFAULT 'app1'` | Target Cloud Run managed service identifier. |
| `secrets_bind` | `LIST` | `SECURED` | Secret Manager mapping (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`). |

## Validation & Runtime Rules

1. **Image Footprint**: Container image compilation must enforce multi-stage or minimal base construction to maintain under 250MB size.
2. **Non-Root Execution**: Container execution must run under non-root UID 10001 (`appuser`).
3. **Secret Isolation**: Container images must not contain hardcoded plaintext database credentials.
