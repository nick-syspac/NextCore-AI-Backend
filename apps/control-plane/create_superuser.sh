#!/bin/bash
# Create a Django superuser with environment variables loaded

set -a
source ../../.env
set +a

python3 manage.py createsuperuser
