# ---------- Stage 1: build the React/Vite app ----------
# node:20-slim (Debian/glibc) is used instead of Alpine: Rollup crashes on musl with "Code is nested too deeply"
FROM node:20-slim AS build

WORKDIR /app

# Cache the dependency layer separately from the source
COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# ---------- Stage 2: serve static files with Nginx ----------
FROM nginx:1.27-alpine

# Reverse-proxy config: serves the SPA and forwards /api and /health to the "backend" service
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Only the compiled production artifacts are copied; Node, node_modules and sources stay in the build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
