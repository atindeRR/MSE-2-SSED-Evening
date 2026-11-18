# Stage 1: Build stage
FROM node:20-slim AS builder

WORKDIR /app

# Copy dependency definition files
COPY package*.json ./

# Install all dependencies (including devDependencies required for build)
RUN npm install

# Copy application source code
COPY . .

# Build production assets
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27-alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts from builder stage to Nginx web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose web server port
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

