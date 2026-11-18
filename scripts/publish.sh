#!/usr/bin/env bash
# Task 3: build, tag (v1 + latest) and push both images to Docker Hub.
# Requires: docker login (or DOCKERHUB_TOKEN in the environment).
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -z "${DOCKERHUB_USERNAME:-}" ] && [ -f .env ]; then
  DOCKERHUB_USERNAME="$(grep -E '^DOCKERHUB_USERNAME=' .env | cut -d= -f2-)"
fi
: "${DOCKERHUB_USERNAME:?Set DOCKERHUB_USERNAME or add it to .env}"

echo "Publishing images for Docker Hub user: $DOCKERHUB_USERNAME"

if [ -n "${DOCKERHUB_TOKEN:-}" ]; then
  printf '%s' "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin
else
  docker login --username "$DOCKERHUB_USERNAME"
fi

docker build -t "$DOCKERHUB_USERNAME/backend:v1" \
             -t "$DOCKERHUB_USERNAME/backend:latest" ./backend
docker build -t "$DOCKERHUB_USERNAME/frontend:v1" \
             -t "$DOCKERHUB_USERNAME/frontend:latest" ./frontend

for image in backend frontend; do
  docker push "$DOCKERHUB_USERNAME/$image:v1"
  docker push "$DOCKERHUB_USERNAME/$image:latest"
done

echo "Published:"
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' |
  grep -E "REPOSITORY|$DOCKERHUB_USERNAME/(backend|frontend)"
