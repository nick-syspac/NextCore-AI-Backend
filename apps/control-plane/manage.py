#!/usr/bin/env python
import os, sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control_plane.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
