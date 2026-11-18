# =============================================================================
# Stage 1 – Build
# Install all dependencies (including devDependencies) and run Vite build.
# Output lands in /app/dist (Vite default; no outDir override in vite.config.js).
# =============================================================================
FROM node:22-slim AS builder

WORKDIR /app

# Copy package.json first so the npm install layer is cached separately
COPY package.json package-lock.json ./

# Install all dependencies (devDependencies are needed to run vite build)
RUN npm ci

# Copy the remaining source files needed for the build
COPY index.html vite.config.js ./
COPY src/ ./src/

# Produce the production build → /app/dist
RUN npm run build

# =============================================================================
# Stage 2 – Production runtime
# Use lightweight Nginx Alpine; copy only the compiled static assets and the
# existing nginx.conf which proxies /api/ and /health to backend:3000.
# =============================================================================
FROM nginx:1.27-alpine

# Replace the default Nginx site config with the project-provided one.
# nginx.conf proxies /api/ → http://backend:3000/api/
#             /health    → http://backend:3000/health
#             /          → index.html (SPA fallback)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the Vite build output into the Nginx web root
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
