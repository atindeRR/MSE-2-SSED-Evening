# Stage 1: Build stage
FROM node:20-slim AS build

WORKDIR /app

# Copy dependency specifications
COPY package*.json ./

# Install dependencies (respects lockfile if present)
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy application source code
COPY . .

# Build production assets using Vite
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27-alpine

# Copy built static assets to Nginx default document root
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing and API reverse proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx server in the foreground
CMD ["nginx", "-g", "daemon off;"]
