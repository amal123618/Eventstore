"""
PythonAnywhere WSGI configuration file for the Eventstore Django project.

PythonAnywhere expects this exact path as the WSGI file in the Web tab.
Point the "WSGI configuration file" field to:
  /home/amaljith0003/Eventstore/pythonanywhere_wsgi.py
"""

import sys
import os

# ── 1. Add your project root to sys.path ────────────────────────────────────
# Adjust this path if your repo is cloned elsewhere on PythonAnywhere
path = '/home/amaljith0003/Eventstore'
if path not in sys.path:
    sys.path.insert(0, path)

# ── 2. Point Django at the correct settings module ──────────────────────────
os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'

# ── 3. Load the WSGI application ────────────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
