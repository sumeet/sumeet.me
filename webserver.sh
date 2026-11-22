#!/bin/bash
set -eu
cd "$(dirname "$0")"
exec python -m gunicorn site_server:application --bind "0.0.0.0:${PORT}" --workers 1 --threads 4
