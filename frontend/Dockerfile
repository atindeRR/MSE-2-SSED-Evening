# ── Frontend Dockerfile ──────────────────────────────────────────────────────
# Multi-stage build: Node builds React/Vite SPA; Nginx serves static production build.
# hadolint global ignore=DL3008,DL3018

# ── Stage 1: build ───────────────────────────────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependency manifests first to leverage Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --ignore-scripts

# Copy application source files
COPY index.html ./
COPY vite.config.js ./
COPY src/ ./src/

# Generate production build artifacts
RUN npm run build

# ── Stage 2: production Nginx image ─────────────────────────────────────────
FROM nginx:1.27-alpine AS runtime

# Copy custom Nginx configuration (reverse-proxy for /api and /health)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build artifacts from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
