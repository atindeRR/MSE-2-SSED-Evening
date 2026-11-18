# ── Stage 1: install production dependencies ─────────────────────────────────
FROM node:20-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

# ── Stage 2: production image ────────────────────────────────────────────────
FROM node:20-alpine AS production

ENV NODE_ENV=production

WORKDIR /app

# Copy pre-installed modules from previous stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy package manifests and application source only
COPY package*.json ./
COPY src ./src

# Run as non-root user (node user uid=1000 in node:alpine)
USER 1000

EXPOSE 3000

CMD ["npm", "start"]
