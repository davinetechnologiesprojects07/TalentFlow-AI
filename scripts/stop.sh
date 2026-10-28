#!/bin/bash

echo "================================="
echo " Stopping TalentFlow AI"
echo "================================="

docker compose down

if [ $? -eq 0 ]; then
    echo "Application stopped successfully!"
else
    echo "Failed to stop application!"
    exit 1
fi
