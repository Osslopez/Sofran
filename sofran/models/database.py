from typing import Optional
import reflex as rx


# ── Categoría (Sculptures, Jewelry, Paintings) ───────
class Category(rx.Model, table=True):
    name: str
    slug: str                    # ej: "sculptures"
    description: Optional[str] = None


# ── Producto (cada obra de arte) ─────────────────────
class Product(rx.Model, table=True):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: int             # referencia a Category
    is_available: bool = True


# ── Imagen de cada producto ───────────────────────────
class ProductImage(rx.Model, table=True):
    product_id: int              # referencia a Product
    url: str                     # ruta de la imagen
    is_primary: bool = False     # imagen principal del producto

# ── Mensaje de contacto ───────────────────────────────
class ContactMessage(rx.Model, table=True):
    name: str
    email: str
    message: str
    created_at: Optional[str] = None    