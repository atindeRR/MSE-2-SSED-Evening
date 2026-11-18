# ==== Frontend Dockerfile (Multi-stage) ====
# Build stage: use Node 20 slim for glibc Rollup compatibility
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies using lockfile
COPY package.json package-lock.json ./
RUN npm ci

# Copy source files
COPY . ./

# Build Vite application with relative /api proxy URL
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# ==== Runtime stage: Nginx Alpine ====
FROM nginx:stable-alpine

# Remove default html files
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
