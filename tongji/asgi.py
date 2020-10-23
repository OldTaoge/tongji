# File:asgi.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
"""
ASGI config for tongji project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tongji.settings')

application = get_asgi_application()
