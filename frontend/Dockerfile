# Stage 1: Build stage
FROM node:20-slim AS builder

WORKDIR /app

# Copy package definitions
COPY package.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Build production static bundle
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27-alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built production static files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
