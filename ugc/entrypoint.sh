#!/usr/bin/env bash

echo "Waiting Kafka start"
while ! nc -z "${KAFKA_HOST}" "${KAFKA_PORT}"; do
  sleep 1
done
echo "Kafka started"

gunicorn --worker-class gevent --workers 4 --bind "0.0.0.0:5000" --log-level debug main:app