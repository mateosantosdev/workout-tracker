#!/bin/sh
# Run database initialisation first
python init_app.py

# Then start the app with waitress
exec waitress-serve --listen=0.0.0.0:${PORT:-5000} run:app
