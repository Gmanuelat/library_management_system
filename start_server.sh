#!/bin/bash

# Library Management System - Server Startup Script

cd "$(dirname "$0")"

echo "========================================="
echo "  Library Management System"
echo "========================================="
echo ""

# Check if data exists, if not run demo to populate
if [ ! -f "data/library.db" ] || [ $(sqlite3 data/library.db "SELECT COUNT(*) FROM Books;" 2>/dev/null || echo "0") -eq 0 ]; then
    echo "Populating database with sample data..."
    cd src && python3 quick_demo.py > /dev/null 2>&1
    cd ..
    echo "✓ Database populated"
fi

echo "Starting Flask server on http://localhost:5001"
echo "Press CTRL+C to stop"
echo ""

# Start Flask server
export FLASK_APP=src.api.app
flask run --host 0.0.0.0 --port 5001
