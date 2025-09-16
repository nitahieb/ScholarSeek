#!/bin/bash

# Build and run the PubMed Author Finder with React frontend

set -e

echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Starting Flask server with React frontend..."
cd src
python webapp.py