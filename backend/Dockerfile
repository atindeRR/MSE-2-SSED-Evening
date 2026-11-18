# syntax=docker/dockerfile:1

# ---- Dependency stage: production dependencies only ----
FROM node:22-alpine AS deps
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# ---- Runtime stage: minimal image with app source only ----
FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --chown=1000:1000 package.json ./
COPY --chown=1000:1000 src ./src

USER 1000:1000

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=6 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:3000/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
