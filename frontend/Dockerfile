# ==========================================
# Frontend Multi-Stage Dockerfile
# Stage 1: Build stage
# Stage 2: Production runtime with Nginx
# ==========================================

# Stage 1: Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package descriptors
COPY package*.json ./

# Install all dependencies required for building
RUN npm install

# Copy application source files
COPY . .

# Build production artifacts (creates dist or build folder)
RUN npm run build

# ==========================================
# Stage 2: Production Runtime Stage
# ==========================================
FROM nginx:alpine AS runner

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built production assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Health check for Frontend Nginx
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
