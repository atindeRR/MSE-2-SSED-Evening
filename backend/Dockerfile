# syntax=docker/dockerfile:1

# ---------- Stage 1: production dependencies only ----------
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund

# ---------- Stage 2: minimal runtime image ----------
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production

COPY --from=deps /app/node_modules ./node_modules
COPY --chown=1000:1000 package.json ./
COPY --chown=1000:1000 src ./src
COPY --chown=1000:1000 db ./db

# Numeric UID/GID 1000 = node in node:20-alpine (also keeps hadolint DL3066 clean).
USER 1000:1000
EXPOSE 3000
CMD ["node", "src/server.js"]
