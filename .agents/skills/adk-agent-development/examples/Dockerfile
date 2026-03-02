# Cloud Run Deployment Dockerfile (Codelab 4 Pattern)
#
# Uses uv for fast dependency management and uvicorn to serve the FastAPI app.
#
# Reference: https://codelabs.developers.google.com/deploy-manage-observe-adk-cloud-run

FROM python:3.12-slim

RUN pip install --no-cache-dir uv==0.7.13

WORKDIR /app
COPY . .

RUN uv sync --frozen

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
