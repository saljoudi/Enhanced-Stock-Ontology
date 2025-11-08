#!/bin/bash

# Enhanced Ontology Dashboard - Render Deployment Script

echo "🚀 Starting Enhanced Ontology Dashboard on Render..."

# Set the port from environment variable or default to 8050
PORT=${PORT:-8050}

# Start the dashboard
gunicorn enhanced_dashboard:server \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class gthread \
    --threads 2 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info