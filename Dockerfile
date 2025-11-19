FROM python:3.13-slim

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    bash \
    netcat-openbsd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set working directory
WORKDIR /code

# Accept build argument to switch between requirements files
ARG REQUIREMENTS=requirements.txt

# Copy the appropriate requirements file
COPY ${REQUIREMENTS} /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the full app source code
COPY . /code/

# Entry point
ENTRYPOINT ["bash", "docker-entrypoint.sh"]
