# ── Stage 1: build ──────────────────────────────────────────────────────────
# Use Debian-based Node for the build stage to get a larger default stack size,
# which is required by Rollup's parser when bundling React on Alpine.
FROM node:20-slim AS build

WORKDIR /app

# Install dependencies first (layer-cache optimisation)
COPY package*.json ./
# Install deps, then pin rollup to 4.9.x (pre-regression) and vite to 5.4.11
RUN npm install && \
    npm install rollup@4.9.6 vite@5.4.11 --no-audit --save-dev

# Copy source and build
COPY . .
RUN npm run build

# ── Stage 2: production runtime ──────────────────────────────────────────────
FROM nginx:1.27-alpine AS production

# Replace default Nginx config with application-specific config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the compiled artefacts from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1/"]
