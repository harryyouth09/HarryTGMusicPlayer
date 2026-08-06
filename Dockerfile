FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /MusicPlayer

# Copy requirements
COPY requirements.txt /MusicPlayer/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . /MusicPlayer

# Make startup script executable
RUN chmod +x /MusicPlayer/startup.sh

# Start bot
CMD ["/bin/bash", "/MusicPlayer/startup.sh"]
