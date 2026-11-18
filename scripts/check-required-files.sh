#!/usr/bin/env bash
set -e

required_files=(
  "backend/Dockerfile"
  "frontend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  ".github/workflows/cd.yml"
)

echo "Checking required files..."
for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "  [OK] $file exists"
  else
    echo "  [FAIL] $file is missing"
    exit 1
  fi
done

echo "All required files are present."
