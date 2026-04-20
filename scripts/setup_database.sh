#!/bin/bash
# Automated database setup for sdd-adk-agents-agy codelab.
# Creates Cloud SQL instance, database, seeds data, generates embeddings,
# and starts MCP Toolbox — all in one script.
#
# Usage: ./scripts/setup_database.sh > database_setup.log 2>&1 &

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "ERROR: .env file not found."
    exit 1
fi

# Validate required variables
for var in GOOGLE_CLOUD_PROJECT REGION DB_PASSWORD; do
    if [ -z "${!var}" ]; then
        echo "ERROR: $var is not set. Check your .env file."
        exit 1
    fi
done

INSTANCE_NAME="restaurant-db"
DATABASE_NAME="restaurant_db"

echo "================================================"
echo "Database Setup"
echo "================================================"
echo ""

# --- Step 1: Create Cloud SQL instance ---
echo "[1/6] Creating Cloud SQL instance..."

# Check if instance already exists
EXISTING=$(gcloud sql instances describe $INSTANCE_NAME --format="value(state)" 2>/dev/null || echo "NOT_FOUND")

if [ "$EXISTING" = "RUNNABLE" ]; then
    echo "      ✓ Instance already exists and is RUNNABLE"
elif [ "$EXISTING" = "NOT_FOUND" ]; then
    gcloud sql instances create $INSTANCE_NAME \
        --database-version=POSTGRES_17 \
        --edition=ENTERPRISE \
        --region=${REGION} \
        --availability-type=ZONAL \
        --tier=db-custom-1-3840 \
        --root-password=${DB_PASSWORD} \
        --enable-google-ml-integration \
        --database-flags cloudsql.enable_google_ml_integration=on \
        --quiet
    echo "      ✓ Instance created"
else
    echo "      Instance state: $EXISTING — waiting for RUNNABLE..."
fi

# --- Step 2: Check whether the instance is ready ---
echo "[2/5] Verifying instance state..."

STATE=$(gcloud sql instances describe "$INSTANCE_NAME" --format='value(state)')

if [ "$STATE" != "RUNNABLE" ]; then
    echo "ERROR: Instance not ready (state: $STATE)"
    exit 1
fi
echo "      ✓ Instance is RUNNABLE"
echo ""

# --- Step 3: Grant Vertex AI permissions ---
echo "[3/6] Granting Vertex AI permissions..."
SERVICE_ACCOUNT=$(gcloud sql instances describe $INSTANCE_NAME --format="value(serviceAccountEmailAddress)")
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/aiplatform.user" \
    --quiet > /dev/null 2>&1
echo "      ✓ Permissions granted"

# --- Step 4: Create database ---
echo "[4/6] Creating database..."

# Check if database already exists
if gcloud sql databases describe "$DATABASE_NAME" \
    --instance="$INSTANCE_NAME" --quiet >/dev/null 2>&1; then
    echo "      Database already exists"
else
    gcloud sql databases create "$DATABASE_NAME" \
        --instance="$INSTANCE_NAME" \
        --quiet
fi

echo "      ✓ Database '$DATABASE_NAME' ready"
echo ""

# --- Step 5: Seed database ---
echo "[5/6] Seeding database and generating embeddings..."
uv run scripts/seed_db.py
echo "      ✓ Database seeded with embeddings"

# --- Step 6: Run the MCP toolbox
echo "[6/6] Running MCP Toolbox..."
npx -y @toolbox-sdk/server --config tools.yaml
echo "      ✓ MCP Toolbox running"

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "Instance:  $INSTANCE_NAME"
echo "Database:  $DATABASE_NAME"
echo "Toolbox:   http://127.0.0.1:5000 (PID: $TOOLBOX_PID)"
echo ""
echo "Monitor Toolbox: tail -f toolbox_server.log"
