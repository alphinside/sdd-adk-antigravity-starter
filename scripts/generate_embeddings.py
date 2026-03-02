"""Generate embeddings for all menu items using Cloud SQL's built-in embedding function.

Uses the google_ml_integration extension to call gemini-embedding-001 directly
from SQL, producing 3072-dimensional vectors stored in the embedding column.
"""

import os
from google.cloud.sql.connector import Connector
import pg8000


def get_connection():
    """Create a connection to Cloud SQL using the Python connector."""
    connector = Connector()
    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    region = os.environ.get("REGION", "us-central1")
    instance_connection = f"{project}:{region}:restaurant-db"

    conn = connector.connect(
        instance_connection,
        "pg8000",
        user="postgres",
        password=os.environ.get("DB_PASSWORD", "codelabpassword"),
        db="restaurant_db",
    )
    return conn


def generate_embeddings():
    """Generate embeddings for menu items that don't have one yet."""
    conn = get_connection()
    cursor = conn.cursor()

    # Count items needing embeddings
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE embedding IS NULL")
    pending = cursor.fetchone()[0]

    if pending == 0:
        print("All menu items already have embeddings.")
        cursor.close()
        conn.close()
        return

    print(f"Generating embeddings for {pending} menu items...")

    # Update embeddings using the in-database embedding function
    cursor.execute("""
        UPDATE menu_items
        SET embedding = embedding('gemini-embedding-001', description)::vector
        WHERE embedding IS NULL
    """)

    rows_updated = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Generated embeddings for {rows_updated} menu items.")


if __name__ == "__main__":
    generate_embeddings()
