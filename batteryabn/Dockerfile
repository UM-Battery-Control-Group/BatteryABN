FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    build-essential \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/batteryabn

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]