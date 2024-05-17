#!/bin/bash

cd /opt/zalando_bot

docker-compose down
docker system prune -f
docker-compose up -d --build

echo "Deploy completed!"
