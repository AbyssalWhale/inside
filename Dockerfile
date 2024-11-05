# Commands
# build: docker build -t python-tests .
# run regression: docker run --rm -v $(pwd)/tests-results:/app/tests-results python-tests pytest -m regression --junitxml=tests-results/junit-test-results.xml

# Start from a Python base image
FROM python:3.13

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install
RUN playwright install-deps

# Copy the application code to the container
COPY . .

# Create a directory for test results
RUN mkdir -p tests-results

# Default command (can be overridden when running the container)
CMD ["pytest"]