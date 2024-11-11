# Commands
# build: docker build -t python-tests .
# run regression: docker run --rm -v $(pwd)/tests-results:/app/tests-results python-tests pytest -m regression --junitxml=tests-results/junit-test-results.xml

FROM python:3.13

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

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

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install
RUN playwright install-deps

COPY . .
COPY runner.py .

RUN mkdir -p /app/tests-results && chown -R 1000 /app/tests-results

CMD ["python", "runner.py"]