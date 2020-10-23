# File:wsgi.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
"""
WSGI config for tongji project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tongji.settings')

application = get_wsgi_application()
