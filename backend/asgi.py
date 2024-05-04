from os import environ

from django.core.asgi import get_asgi_application

environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="backend.settings")

application = get_asgi_application()
