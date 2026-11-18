# ── Backend Dockerfile ──────────────────────────────────────────────────────
# Multi-stage build: install dependencies in deps stage, copy to lean production image.

# ── Stage 1: dependency installation ────────────────────────────────────────
FROM node:22-alpine AS dependencies

WORKDIR /app

# Copy package manifests
COPY package.json package-lock.json ./

# Install production dependencies only
RUN npm ci --omit=dev --ignore-scripts

# ── Stage 2: production runtime ──────────────────────────────────────────────
FROM node:22-alpine AS production

ENV NODE_ENV=production
WORKDIR /app

# Copy production node_modules from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy application source and database scripts
COPY package.json ./
COPY src/ ./src/
COPY db/  ./db/

# Use the built-in non-root node user (UID:GID 1000:1000)
USER 1000:1000

EXPOSE 3000

CMD ["node", "src/server.js"]
