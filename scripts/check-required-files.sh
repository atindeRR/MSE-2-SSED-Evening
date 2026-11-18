#!/usr/bin/env bash
set -e

echo "=== Verifying Required Submission Files ==="

REQUIRED_FILES=(
  "submission.json"
  "backend/Dockerfile"
  "frontend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  ".github/workflows/cd.yml"
)

MISSING=0

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  [OK] $file exists"
  else
    echo "  [ERROR] Missing required file: $file"
    MISSING=1
  fi
done

# Check for PDF report
PDF_COUNT=$(find . -maxdepth 1 -name "*_SET2.pdf" -o -name "*.pdf" | grep -v "MSE-2_Evening" | wc -l)
if [ "$PDF_COUNT" -gt 0 ]; then
  echo "  [OK] Mandatory PDF report found"
else
  echo "  [WARNING] No candidate PDF report found matching *_SET2.pdf"
fi

if [ "$MISSING" -ne 0 ]; then
  echo "Validation FAILED: Required files are missing."
  exit 1
fi

echo "All required files are verified successfully!"
exit 0
