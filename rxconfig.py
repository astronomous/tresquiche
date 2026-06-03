import reflex as rx
from reflex.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="tres_quiche",
    show_built_with_reflex=False,
    disable_plugins=[SitemapPlugin],
)
