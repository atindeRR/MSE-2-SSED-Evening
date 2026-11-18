#!/bin/bash
set -e

echo "=== Checking Required Deliverables ==="

required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  ".github/workflows/cd.yml"
)

missing=0

for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file"
  else
    echo "✗ Missing: $file"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "Error: One or more required files are missing."
  exit 1
fi

echo "=== All required deliverables are present ==="
exit 0
