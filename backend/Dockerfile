# syntax=docker/dockerfile:1

FROM node:22-alpine AS base
WORKDIR /app

# Install only production dependencies
COPY package.json ./
RUN npm install --omit=dev && npm cache clean --force

# Copy application source (honours .dockerignore)
COPY src/ ./src/

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "src/server.js"]
