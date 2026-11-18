# ── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# NODE_ENV must NOT be "production" here — devDependencies (vite, @vitejs/plugin-react)
# are required to compile the app. We set it explicitly so that any parent-image or
# CI environment default cannot silently skip them.
ENV NODE_ENV=development

# Copy manifests + lockfile first for layer-cache efficiency.
# npm ci: deterministic, uses exact versions from package-lock.json, includes devDeps.
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the source tree (index.html, src/, vite.config.js, etc.)
COPY . .

# Compile — Vite 5.4.0 (pinned) outputs to /app/dist
RUN npm run build

# ── Stage 2: Serve ───────────────────────────────────────────────────────────
FROM nginx:1.27-alpine

# Remove default Nginx placeholder content
RUN rm -rf /usr/share/nginx/html/*

# Copy the compiled static bundle from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Use the project-supplied Nginx config (proxies /api → backend:3000)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
