"""Seed the restaurant database with schema and initial menu data.

Uses cloud-sql-python-connector to connect directly to Cloud SQL
without needing Cloud SQL Auth Proxy or psql.
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


def create_schema(cursor):
    """Create the database schema."""
    print("Creating extensions...")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS google_ml_integration;")

    print("Creating menu_items table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            dietary_tags TEXT[] DEFAULT '{}',
            embedding vector(3072),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def seed_menu(cursor):
    """Insert seed menu data."""
    menu_items = [
        (
            "Truffle Mushroom Bruschetta",
            "appetizers",
            "Crispy sourdough topped with sauteed wild mushrooms, truffle oil, and shaved Parmesan.",
            14.50,
            "{vegetarian}",
        ),
        (
            "Tuna Tartare",
            "appetizers",
            "Fresh ahi tuna with avocado, sesame, soy-ginger dressing, and wonton crisps.",
            16.00,
            "{}",
        ),
        (
            "Roasted Beet Salad",
            "appetizers",
            "Golden and red beets with goat cheese, candied walnuts, and citrus vinaigrette.",
            12.00,
            "{vegetarian,gluten-free}",
        ),
        (
            "Crispy Calamari",
            "appetizers",
            "Lightly breaded calamari rings with marinara dipping sauce and lemon wedges.",
            13.00,
            "{}",
        ),
        (
            "Grilled Salmon",
            "entrees",
            "Atlantic salmon fillet with lemon-dill sauce, roasted asparagus, and fingerling potatoes.",
            28.00,
            "{gluten-free}",
        ),
        (
            "Braised Short Ribs",
            "entrees",
            "Slow-braised beef short ribs with red wine reduction, creamy polenta, and root vegetables.",
            32.00,
            "{gluten-free}",
        ),
        (
            "Wild Mushroom Risotto",
            "entrees",
            "Arborio rice with porcini and chanterelle mushrooms, white wine, and aged Parmesan.",
            24.00,
            "{vegetarian,gluten-free}",
        ),
        (
            "Pan-Seared Duck Breast",
            "entrees",
            "Duck breast with cherry gastrique, sweet potato puree, and sauteed greens.",
            30.00,
            "{gluten-free}",
        ),
        (
            "Herb-Crusted Rack of Lamb",
            "entrees",
            "New Zealand lamb rack with rosemary-garlic crust, mint pesto, and roasted vegetables.",
            36.00,
            "{}",
        ),
        (
            "Grilled Vegetable Tower",
            "entrees",
            "Stacked grilled zucchini, eggplant, bell peppers, and portobello with romesco sauce.",
            22.00,
            "{vegan,gluten-free}",
        ),
        (
            "Chocolate Lava Cake",
            "desserts",
            "Warm dark chocolate cake with a molten center, served with vanilla bean ice cream.",
            12.00,
            "{vegetarian}",
        ),
        (
            "Creme Brulee",
            "desserts",
            "Classic vanilla custard with a caramelized sugar crust and fresh berries.",
            10.00,
            "{vegetarian,gluten-free}",
        ),
        (
            "Lemon Tart",
            "desserts",
            "Buttery pastry filled with tangy lemon curd, topped with toasted meringue.",
            11.00,
            "{vegetarian}",
        ),
        (
            "Sparkling Elderflower Lemonade",
            "drinks",
            "Refreshing house-made lemonade with elderflower syrup and sparkling water.",
            6.00,
            "{vegan,gluten-free}",
        ),
        (
            "Classic Espresso Martini",
            "drinks",
            "Vodka, fresh espresso, coffee liqueur, and simple syrup shaken over ice.",
            14.00,
            "{vegan,gluten-free}",
        ),
        (
            "Fresh Mint Iced Tea",
            "drinks",
            "Cold-brewed black tea with fresh mint leaves and a touch of honey.",
            5.00,
            "{vegan,gluten-free}",
        ),
    ]

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Menu already has {count} items — skipping seed data.")
        return

    print(f"Inserting {len(menu_items)} menu items...")
    for name, category, description, price, tags in menu_items:
        cursor.execute(
            """INSERT INTO menu_items (name, category, description, price, dietary_tags)
               VALUES (%s, %s, %s, %s, %s::text[])""",
            (name, category, description, price, tags),
        )

    print(f"Seeded {len(menu_items)} menu items.")


def main():
    conn = get_connection()
    cursor = conn.cursor()

    create_schema(cursor)
    seed_menu(cursor)

    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
