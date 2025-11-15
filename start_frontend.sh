#!/bin/bash

# AI MemeForge Frontend Startup Script

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the dev server
echo "Starting AI MemeForge Frontend..."
echo "Frontend will be available at: http://localhost:5173"
echo ""
npm run dev

