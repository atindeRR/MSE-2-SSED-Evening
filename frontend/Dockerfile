# Multi-stage build for React frontend application

# Stage 1: Build static assets using Node.js
FROM node:20-slim AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source files and build
COPY . .
RUN npm run build

# Stage 2: Production runtime with lightweight Nginx web server
FROM nginx:1.27-alpine AS production

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static artifacts from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose web server port
# Expose web server port
EXPOSE 80

# Health check to verify Nginx is serving content
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/"]