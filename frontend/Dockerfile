# ── Stage 1: Build (Debian-based for larger C stack — fixes Rollup parser) ──
FROM node:22-slim AS builder

WORKDIR /app

# Install dependencies first (leverages layer cache)
COPY package.json ./
RUN npm install

# Copy source and build production assets
COPY . .
RUN npm run build

# ── Stage 2: Serve ──────────────────────────────────────────────────────────
FROM nginx:1.27-alpine AS production

# Remove the default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration (reverse-proxies /api/* to backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
