# syntax=docker/dockerfile:1

# ---- Build stage: compile the Vite/React app ----
FROM node:22-alpine AS build
WORKDIR /app

# Install dependencies first so this layer is cached while source changes.
COPY package.json package-lock.json ./
RUN npm ci && npm cache clean --force

COPY . .
RUN npm run build

# ---- Runtime stage: serve static assets with nginx ----
FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
