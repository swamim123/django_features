# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import MyConsumer  # Adjust with your actual consumer

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            [
                path("ws/", MyConsumer.as_asgi()),
            ]
        ),
        # Add other protocols as needed
    }
)