#!/bin/bash

echo "================================="
echo " Building TalentFlow AI"
echo "================================="

docker compose build

if [ $? -eq 0 ]; then
    echo "Build successful!"
else
    echo "Build failed!"
    exit 1
fi
