# syntax=docker/dockerfile:1

# Stage 1: install production-only dependencies from the committed lockfile.
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Stage 2: runtime image containing only the application source and production modules.
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./
COPY src ./src
COPY db ./db

EXPOSE 3000

# The API already binds 0.0.0.0 (see src/server.js) and /health checks PostgreSQL + Redis.
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:3000/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

USER 1000
CMD ["npm", "start"]
