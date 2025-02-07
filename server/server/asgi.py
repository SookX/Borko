import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import assistant.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

print("ASGI application loaded!")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
     "websocket": URLRouter(assistant.routing.websocket_urlpatterns),
})
