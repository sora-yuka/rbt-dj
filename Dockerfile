FROM python:3.13.13-trixie

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]
