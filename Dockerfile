# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the startup script into the container
COPY start_and_download.sh /app/start_and_download.sh

# Make the script executable
RUN chmod +x /app/start_and_download.sh

# Expose port 5000
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the startup script
CMD ["/app/start_and_download.sh"]
