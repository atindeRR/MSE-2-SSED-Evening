# ---------------------------------------------------------------
# Stage 1 - build: compile the React/Vite app with Node.js
# (Debian "slim" variant: Vite/Rollup's native parser needs glibc;
#  this stage is thrown away, so its size does not matter)
# ---------------------------------------------------------------
FROM node:22-slim AS build

WORKDIR /app

# Copy manifests first for layer caching, then install all deps
# (Vite and the React plugin are devDependencies needed to build).
COPY package.json package-lock.json ./
RUN npm ci

# Copy the source and produce the static production bundle in /app/dist
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

# ---------------------------------------------------------------
# Stage 2 - runtime: serve only the built files with Nginx
# ---------------------------------------------------------------
FROM nginx:1.27-alpine AS runtime

# Nginx config: serves the SPA and reverse-proxies /api and /health
# to the "backend" service over the Docker network.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy ONLY the compiled artifacts - no node_modules, no source code
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
