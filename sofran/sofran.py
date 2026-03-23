import reflex as rx
import sqlmodel
from sofran.models.database import Category, Product, ProductImage, ContactMessage

# ── Colores ──────────────────────────────────────────
GREEN    = "#3a7a5e"     # verde solo para acentos pequeños
BG       = "#0a0a0a"    # negro casi puro
CARD     = "#111111"    # gris muy oscuro
CARD2    = "#161616"
MUTED    = "#888888"    # gris para textos secundarios
TEXT_DIM = "#555555"
LILAC    = "#3a7a5e"    # acento verde suave

# ── State ─────────────────────────────────────────────
class GalleryState(rx.State):
    products: list[dict] = []

    def load_products(self, slug: str):
        with rx.session() as session:
            category = session.exec(
                sqlmodel.select(Category).where(Category.slug == slug)
            ).first()

            if category:
                items = session.exec(
                    sqlmodel.select(Product).where(
                        Product.category_id == category.id
                    )
                ).all()

                self.products = [
                    {
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                    }
                    for p in items
                ]

class ContactState(rx.State):
    name: str = ""
    email: str = ""
    message: str = ""
    sent: bool = False

    def set_name(self, value: str):
        self.name = value

    def set_email(self, value: str):
        self.email = value

    def set_message(self, value: str):
        self.message = value

    def send_message(self):
        with rx.session() as session:
            session.add(
                ContactMessage(
                    name=self.name,
                    email=self.email,
                    message=self.message,
                )
            )
            session.commit()

        self.name = ""
        self.email = ""
        self.message = ""
        self.sent = True

# ── Componentes ──────────────────────────────────────
def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.text(
    "SOFRAN",
    letter_spacing="0.3em",
    color="#a3c4b5",
    font_family="Cormorant Garamond, serif",
    font_size="22px",
    font_weight="300",
),
            href="/",
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Sculptures", href="/sculptures"),
            rx.link("Jewelry",    href="/jewelry"),
            rx.link("Paintings",  href="/paintings"),
            rx.link("Contact",    href="/contact"),
            spacing="6",
        ),
        width="100%",
        padding="20px 60px",
    )


def hero() -> rx.Component:
    return rx.vstack(
        rx.heading(
    "Art born from shadow and nature",
    size="8",
    text_align="center",
    max_width="700px",
    font_family="Cormorant Garamond, serif",
    font_weight="300",
    letter_spacing="0.05em",
),
        rx.text(
    "Handcrafted works by Annabella Sofran.",
    color="#666666",
    font_size="18px",
    letter_spacing="0.1em",
),
        rx.button(
            " View Collections ",
            bg="transparent",
            border="1px solid #2c8165",
            color="#8993A3",
            padding="12px 32px",
            _hover={"bg": "#1a1a22"},
        ),
        spacing="6",
        align="center",
        padding_y="120px",
    )


def minimal_card(title: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(title, color="white"),
            rx.box(height="1px", width="40px", bg=GREEN),
            spacing="4",
            align="start",
        ),
        padding="40px",
        bg=CARD,
        width="260px",
        border_radius="12px",
        _hover={"bg": "#1b1b24", "transition": "0.3s"},
    )


def categories() -> rx.Component:
    return rx.hstack(
        minimal_card("Creepy Sculptures"),
        minimal_card("Dark Jewelry"),
        minimal_card("Organic Paintings"),
        spacing="8",
        justify="center",
        padding_bottom="80px",
        flex_wrap="wrap",
    )


def product_card(product: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                bg="#1b1b24",
                height="200px",
                width="100%",
                border_radius="8px 8px 0 0",
            ),
            rx.vstack(
                rx.text(
                    product["name"],
                    color="white",
                    font_weight="bold",
                ),
                rx.text(
                    product["description"],
                    color="#888",
                    font_size="14px",
                ),
                rx.text(
                    "$" + product["price"].to_string(),
                    color=MUTED,
                    font_size="16px",
                ),
                spacing="2",
                align="start",
                padding="16px",
            ),
            spacing="0",
        ),
        bg=CARD,
        border_radius="10px",
        _hover={
            "transform": "scale(1.03)",
            "transition": "0.3s",
        },
    )


def gallery_page(title: str, slug: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.heading(title, size="8", padding_top="60px"),
            rx.grid(
                rx.foreach(
                    GalleryState.products,
                    product_card,
                ),
                columns="3",
                spacing="6",
                padding="60px",
                width="100%",
            ),
            spacing="8",
            align="center",
            width="100%",
        ),
        bg=BG,
        color="white",
        min_height="100vh",
        on_mount=GalleryState.load_products(slug),
    )

# ── Páginas ───────────────────────────────────────────
def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            hero(),
            categories(),
            spacing="9",
            align="center",
            width="100%",
        ),
        bg=BG,
        color="white",
        min_height="100vh",
    )


def sculptures() -> rx.Component:
    return gallery_page("Creepy Sculptures", "sculptures")


def jewelry() -> rx.Component:
    return gallery_page("Dark Jewelry", "jewelry")


def paintings() -> rx.Component:
    return gallery_page("Organic Paintings", "paintings")

def contact() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.vstack(
                rx.heading(
                    "Get in touch",
                    size="8",
                    text_align="center",
                ),
                rx.text(
                    "Commission a piece or ask about availability.",
                    color="#888",
                    text_align="center",
                ),
                rx.cond(
                    ContactState.sent,
                    rx.text(
                        "✅ Message sent! I'll get back to you soon.",
                        color=GREEN,
                        font_size="16px",
                    ),
                    rx.vstack(
                        rx.input(
                            placeholder="Your name",
                            value=ContactState.name,
                            on_change=ContactState.set_name,
                            bg=CARD,
                            border="1px solid #333",
                            color="white",
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Your email",
                            value=ContactState.email,
                            on_change=ContactState.set_email,
                            bg=CARD,
                            border="1px solid #333",
                            color="white",
                            width="100%",
                        ),
                        rx.text_area(
                            placeholder="Your message",
                            value=ContactState.message,
                            on_change=ContactState.set_message,
                            bg=CARD,
                            border="1px solid #333",
                            color="white",
                            width="100%",
                            rows="6",
                        ),
                        rx.button(
                            "Send Message",
                            on_click=ContactState.send_message,
                            bg=LILAC,
                            color="white",
                            width="100%",
                            _hover={"bg": "#7a4db8"},
                        ),
                        spacing="4",
                        width="100%",
                    ),
                ),
                spacing="6",
                width="500px",
                padding_y="80px",
            ),
            align="center",
            width="100%",
        ),
        bg=BG,
        color="white",
        min_height="100vh",
    )

# ── App ───────────────────────────────────────────────
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Raleway:wght@300;400;500&display=swap",
        "/style.css",
    ]
)  # pylint: disable=not-callable

app.add_page(index,      route="/")
app.add_page(sculptures, route="/sculptures")
app.add_page(jewelry,    route="/jewelry")
app.add_page(paintings,  route="/paintings")
app.add_page(contact, route="/contact")