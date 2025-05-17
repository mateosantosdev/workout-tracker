#!/bin/sh
# Run database initialisation first
python -m app.init_app

# Then start the app with waitress
exec waitress-serve --listen=0.0.0.0:${PORT:-5000} run:app
