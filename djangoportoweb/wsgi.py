"""
WSGI config for djangoportoweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoportoweb.settings')

application = get_wsgi_application()


# from whitenoise import WhiteNoise
# application = WhiteNoise(application)
# from whitenoise import WhiteNoise
# from djangoportoweb import wsgi
# application = wsgi()
# application = WhiteNoise(application, root="/namegen/static")
# application.add_files("/namegen/static", prefix="more-files/")