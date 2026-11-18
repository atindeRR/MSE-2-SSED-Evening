# Stage 1: Build stage (using Debian slim with standard glibc stack size for Vite/Rollup)
FROM node:20-slim AS build

WORKDIR /app

# Copy package manifests
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source code
COPY . .

# Build production assets
RUN npm run build

# Stage 2: Production runtime stage (lightweight Nginx Alpine)
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build artifacts from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
