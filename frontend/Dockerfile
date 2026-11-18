# ── Frontend Dockerfile (multi-stage build) ─────────────────────────
# Stage 1 – Build the React app with Vite
# Stage 2 – Serve the static assets with Nginx (lightweight runtime)

# ── Stage 1: build ───────────────────────────────────────────────────
# node:20-slim (Debian) is used here because Alpine (musl libc) can cause
# native-binary issues with Vite / Rollup during the build step.
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy source and build
COPY index.html ./
COPY vite.config.js ./
COPY src/ ./src/

RUN npm run build

# ── Stage 2: production runtime ──────────────────────────────────────
FROM nginx:alpine

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy the production build from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

# Use the custom Nginx config (handles /api proxy + SPA fallback)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
