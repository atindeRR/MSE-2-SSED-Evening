# syntax=docker/dockerfile:1

# ── Stage 1: Build the React app ──────────────────────────────────────────────
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json ./
RUN npm install && npm cache clean --force

COPY package.json .npmrc* ./
COPY index.html vite.config.js ./
COPY src/ ./src/

# Pin rollup via override so Vite uses 4.20.0 (avoids parser depth bug in 4.24+)
RUN npm install rollup@4.20.0 --save-dev --no-fund --no-audit && npm run build

# ── Stage 2: Serve with Nginx ──────────────────────────────────────────────────
FROM nginx:1.27-alpine AS production

# Remove the default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy the custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the production build artifacts from stage 1
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
