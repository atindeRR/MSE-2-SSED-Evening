#!/bin/bash
set -e

echo "Checking required files..."
required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  ".github/workflows/cd.yml"
  "submission.json"
)

for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file"
  else
    echo "✗ Missing required file: $file"
    exit 1
  fi
done

echo "All required files are present."
