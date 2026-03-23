import reflex as rx

# ── Colores ──────────────────────────────────────────
LILAC = "#643E99"
GREEN = "#2c8165"
BG    = "#0b0b10"
MUTED = "#d967dd"
CARD  = "#14141a"


# ── Componentes ──────────────────────────────────────
def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.text("SOFRAN", letter_spacing="0.3em", color="#c46d9d"),
            href="/",
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Sculptures", href="/sculptures"),
            rx.link("Jewelry",    href="/jewelry"),
            rx.link("Paintings",  href="/paintings"),
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
        ),
        rx.text(
            "Handcrafted works by Annabella Sofran.",
            color="#2e5e4e",
            font_size="18px",
        ),
        rx.button(
            "View Collections",
            bg="transparent",
            border="1px solid #c8a2ff",
            color="#c8a2ff",
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


def gallery_page(title: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(title, size="8"),
            rx.grid(
                *[
                    rx.box(
                        bg="#1b1b24",
                        height="250px",
                        border_radius="10px",
                        _hover={
                            "transform": "scale(1.03)",
                            "transition": "0.3s",
                        },
                    )
                    for _ in range(6)
                ],
                columns="3",
                spacing="6",
            ),
            spacing="8",
            padding="60px",
        ),
        bg=BG,
        color="white",
        min_height="100vh",
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
    return gallery_page("Creepy Sculptures")


def jewelry() -> rx.Component:
    return gallery_page("Dark Jewelry")


def paintings() -> rx.Component:
    return gallery_page("Organic Paintings")


# ── App ───────────────────────────────────────────────
app = rx.App(stylesheets=["/style.css"])

app.add_page(index,      route="/")
app.add_page(sculptures, route="/sculptures")
app.add_page(jewelry,    route="/jewelry")
app.add_page(paintings,  route="/paintings")