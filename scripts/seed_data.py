#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.config.settings")

import django
django.setup()

from django.core.management import call_command

if __name__ == "__main__":
    print("Running database migrations...")
    call_command("migrate", interactive=False)
    print("Running database seed command...")
    call_command("seed_dealerships")
    print("Database is fully initialized and seeded!")
