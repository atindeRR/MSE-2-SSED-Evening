# ============================================================
# Stage 1 – build
# Build the Vite / React application and produce the dist/
# ============================================================
FROM node:20-alpine AS build

WORKDIR /app

# Copy manifests first so that this layer is cached when only
# source files change. package-lock.json is copied if present
# (glob pattern includes it when it exists).
COPY package*.json ./

# Use the committed lockfile for a fully reproducible install.
# rollup@4.24.0 is pinned in package-lock.json to work around a
# parser regression in Rollup ≥4.25 (Vite ≥5.4.10) on Node 20.20.
RUN npm ci

# Copy application source and build.
COPY . .
RUN npm run build

# ============================================================
# Stage 2 – production runtime
# Lightweight Nginx image serves the static build artefacts
# and reverse-proxies /api/ and /health to the backend.
# ============================================================
FROM nginx:1.27-alpine AS production

# Replace the default Nginx site config with the custom one
# that handles SPA routing and backend proxying.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the production build output – nothing else.
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx listens on 80 by default.
EXPOSE 80

# Health check: wget is available in the Alpine Nginx image.
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
