# main.py

from app import app

# This exposes the Flask app instance as "app"
# so Cloud Run (via gunicorn main:app) can detect it
