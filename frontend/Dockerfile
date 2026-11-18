# ---------------------------------------------------------------
# Stage 1 - build: compile the React/Vite app with Node.js
# ---------------------------------------------------------------
FROM node:22-slim AS build

WORKDIR /app

# Copy manifests first for layer caching, then install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source files and build the production bundle
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

# ---------------------------------------------------------------
# Stage 2 - runtime: lightweight production web server (Nginx)
# ---------------------------------------------------------------
FROM nginx:1.27-alpine AS runtime

# Nginx reverse proxy and SPA configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the compiled production artifacts into the web root
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# Health check verifying the web server is answering HTTP requests
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
