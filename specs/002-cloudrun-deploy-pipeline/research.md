# Research: Cloud Run Deployment Pipeline & Secure Containerization

## Decisions

### 1. Minimal Base Image & Non-Root Hardening

- **Decision**: Use `python:3.11-slim` as the minimal container base image. Enforce environment variables `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`. Establish a dedicated non-root user `appuser` (UID 10001) to execute the container runtime.
- **Rationale**: `python:3.11-slim` provides a highly optimized Debian-based image footprint (~45MB compressed) without the standard build toolchain overhead. Executing under a dedicated non-root user mitigates privilege escalation vulnerabilities if container escape attempts occur.
- **Alternatives considered**:
  - *python:3.11-alpine*: Rejected because Alpine relies on `musl` libc, which frequently causes binary incompatibility or compilation slowdowns with standard scientific/database Python drivers (e.g., `cloud-sql-python-connector`).

### 2. Cloud Build CI/CD Pipeline

- **Decision**: Define a declarative `cloudbuild.yaml` pipeline configured to trigger automatically on git push events targeting the `main` branch. The build workflow coordinates three primary stages:
  1. Build container image using `docker build -t gcr.io/$PROJECT_ID/fastapi-app:$COMMIT_SHA .`
  2. Push image to Container Registry / Artifact Registry via `docker push`
  3. Deploy revision to Google Cloud Run via `gcloud run deploy fastapi-app`
- **Rationale**: Provides native, highly integrated Google Cloud execution without requiring third-party CI runners. Utilizing `$COMMIT_SHA` tags guarantees distinct, immutable deployment revisions.
- **Alternatives considered**:
  - *GitHub Actions*: Rejected because `cloudbuild.yaml` is explicitly mandated and provides frictionless, IAM-governed Cloud Run and Secret Manager access out of the box.

### 3. Database Credential Handling via Secret Manager

- **Decision**: Inject database authentication parameters (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`) dynamically into the Cloud Run execution environment using Cloud Run's native Secret Manager mapping (`--set-secrets`).
- **Rationale**: Completely isolates static container layers from credential exposure while leveraging automated GCP service account authentication.
- **Alternatives considered**:
  - *Runtime API Lookup inside app*: Rejected as Cloud Run natively populates secrets as in-memory environment variables or volumes without adding runtime SDK lookup code inside the application.
