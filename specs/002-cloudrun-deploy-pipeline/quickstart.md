# Quickstart: Cloud Run Deployment & Container Execution

## 1. Local Container Verification

Build the minimal secure container image locally using Docker:

```bash
docker build -t fastapi-app:local .
```

Verify non-root runtime execution and port binding:

```bash
docker run -d -p 8080:8080 --name local-app \
  -e DATABASE_URL=sqlite+aiosqlite:///:memory: \
  -e RESERVATIONS_API_KEY=secret123 \
  fastapi-app:local
```

Verify container health probe:

```bash
curl http://localhost:8080/health
```

## 2. Cloud Build Pipeline Manual Rollout

Execute the Cloud Build pipeline locally or manually submit to Google Cloud Build:

```bash
gcloud builds submit --config cloudbuild.yaml .
```
