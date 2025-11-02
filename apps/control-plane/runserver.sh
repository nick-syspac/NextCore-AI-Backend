#!/bin/bash
# Load environment variables from .env file and run Django development server

set -a
source ../../.env
set +a

python3 manage.py runserver "$@"
