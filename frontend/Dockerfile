
# Stage 1: Build React application
FROM node:22-alpine AS builder

WORKDIR /app

# Install exact dependency versions from the lock file
COPY package.json package-lock.json ./
RUN npm ci

# Copy application source
COPY . .

# Create production build
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
