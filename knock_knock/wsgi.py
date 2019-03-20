"""
WSGI config for knock_knock project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
# from wsgi_sslify import sslify


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knock_knock.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root='static/')
# application = sslify(application)

#Usefule for adding other static files like profiel images and documents
# application.add_files('/path/to/more/static/files', prefix='more-files/')