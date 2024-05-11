from os import environ

from django.core.wsgi import get_wsgi_application

environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="backend.settings")

application = get_wsgi_application()
