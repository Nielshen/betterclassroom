# Python-Image
FROM python:3.10-slim-buster

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt || echo "Failed to install requirements"

COPY . /app/

# Expose port
EXPOSE 5000

# Start
CMD ["python", "app.py"] || echo "Failed to start app"