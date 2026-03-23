import reflex as rx
from sofran.models.database import Category, Product

def seed():
    with rx.session() as session:

        # ── Categorías ────────────────────────────────
        sculptures = Category(
            name="Creepy Sculptures",
            slug="sculptures",
            description="Dark handcrafted sculptures inspired by nature",
        )
        jewelry = Category(
            name="Dark Jewelry",
            slug="jewelry",
            description="Organic jewelry with dark and natural elements",
        )
        paintings = Category(
            name="Organic Paintings",
            slug="paintings",
            description="Paintings inspired by shadow and nature",
        )

        session.add(sculptures)
        session.add(jewelry)
        session.add(paintings)
        session.commit()

        # ── Productos ─────────────────────────────────
        products = [
            Product(
                name="Spider Web Sculpture",
                description="Handcrafted spider web in dark resin",
                price=180.00,
                category_id=sculptures.id,
            ),
            Product(
                name="Bone Candle Holder",
                description="Organic bone-shaped candle holder",
                price=95.00,
                category_id=sculptures.id,
            ),
            Product(
                name="Forest Ring",
                description="Silver ring with embedded moss",
                price=65.00,
                category_id=jewelry.id,
            ),
            Product(
                name="Dark Moon Necklace",
                description="Black moon pendant with silver chain",
                price=75.00,
                category_id=jewelry.id,
            ),
            Product(
                name="Shadow Forest",
                description="Oil painting of a dark forest at night",
                price=320.00,
                category_id=paintings.id,
            ),
            Product(
                name="Roots",
                description="Acrylic painting of organic roots",
                price=280.00,
                category_id=paintings.id,
            ),
        ]

        for product in products:
            session.add(product)

        session.commit()
        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()