# Stage 1: Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency manifests and install dependencies
COPY package*.json ./
RUN npm ci

# Copy application source code and build production assets
COPY . .
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27-alpine AS production

# Copy custom Nginx configuration for SPA routing and reverse proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build artifacts from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Health check to ensure Nginx server is actively responding
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]

