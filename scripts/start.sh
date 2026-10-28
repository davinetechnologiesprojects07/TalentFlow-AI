#!/bin/bash

echo "================================="
echo " Starting TalentFlow AI"
echo "================================="

docker compose up -d

if [ $? -eq 0 ]; then
    echo "Application started successfully!"
    echo "Open: http://localhost:8081"
else
    echo "Failed to start application!"
    exit 1
fi
