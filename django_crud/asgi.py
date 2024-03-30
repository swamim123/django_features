"""
ASGI config for django_crud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from book import routing

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})
