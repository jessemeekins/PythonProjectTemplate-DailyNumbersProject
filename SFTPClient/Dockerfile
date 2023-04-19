FROM ubuntu:latest

WORKDIR /app

# Update package list and install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Create directory for imports
RUN mkdir /app/imports

# Copy the application code into the container
COPY app.py /app/

# Set the command to be run when the container starts
CMD ["cron", "-f"]
