#!/bin/bash

# Start Flask app in the background
flask run &
FLASK_PID=$!

# Wait for Flask server to start
echo "Waiting for Flask server to start..."
while ! curl -s http://localhost:5000 > /dev/null; do sleep 1; done
echo "Flask server started."

# Download the file
curl http://localhost:5000/metadata/download -o interview.csv

echo "File downloaded."
# Keep the Flask server running in the foreground so the container doesn't exit
wait $FLASK_PID
