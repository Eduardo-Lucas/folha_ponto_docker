#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input
# python manage.py findstatic --verbosity 2 “[foo]”

# Apply any outstanding database migrations
python manage.py makemigrations
python manage.py migrate
