# syntax=docker/dockerfile:1

# Stage 1: compile the production React bundle with Vite.
FROM node:22-alpine AS build
WORKDIR /app

# Install from the committed lockfile before copying source so this layer is cached.
COPY package.json package-lock.json ./
RUN npm ci

# Copy only the inputs Vite needs, then produce /app/dist.
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

# Stage 2: lightweight production web server. No Node toolchain or dev dependencies.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/ /usr/share/nginx/html/

EXPOSE 80

# nginx.conf proxies /api and /health to the backend service on the Compose network.
# The browser therefore only talks to the frontend origin; no CORS/service-name issue.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1/"]
