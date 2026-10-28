#!/bin/bash

echo "================================="
echo " TalentFlow AI Health Check"
echo "================================="

if curl -f http://localhost:8081 > /dev/null 2>&1; then
    echo "TalentFlow AI is UP!"
else
    echo "TalentFlow AI is DOWN!"
    exit 1
fi
