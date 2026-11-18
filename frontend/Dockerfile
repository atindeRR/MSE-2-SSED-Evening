# syntax=docker/dockerfile:1

# ---------- Stage 1: build the production bundle ----------
FROM node:20-alpine AS build
WORKDIR /app

# Install dependencies from the committed lockfile first so this layer is cached.
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY . .
RUN npm run build

# ---------- Stage 2: lightweight production server ----------
FROM nginx:1.27-alpine AS runtime

# Only the compiled static assets ship in the final image.
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Run Nginx as the unprivileged nginx user: pre-create writable paths and
# move the PID file to /tmp (the default /run is root-owned).
RUN mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp \
    && chown -R nginx:nginx /var/cache/nginx \
    && sed -i 's|/run/nginx.pid|/tmp/nginx.pid|' /etc/nginx/nginx.conf

EXPOSE 80
# Numeric UID/GID 101 = nginx in nginx:1.27-alpine (also keeps hadolint DL3066 clean).
USER 101:101
CMD ["nginx", "-g", "daemon off;"]
