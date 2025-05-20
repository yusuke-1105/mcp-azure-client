# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies if a requirements file is provided
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install npm
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    apt-get install -y npm && \
    rm -rf /var/lib/apt/lists/*

# Install azure-cli
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash