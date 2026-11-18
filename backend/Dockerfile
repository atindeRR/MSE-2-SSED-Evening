# ============================================================
# Stage 1 – install production dependencies
# Keeps node_modules separate so the runtime stage never
# receives npm, build tools, or the full npm cache.
# ============================================================
FROM node:20-alpine AS dependencies

WORKDIR /app

# Copy manifests first (layer-cache optimisation).
# package-lock.json is included when present via the glob.
COPY package*.json ./

# Install production dependencies only using the committed lockfile
# for a fully reproducible install (npm ci requires package-lock.json).
RUN npm ci --omit=dev

# ============================================================
# Stage 2 – production runtime
# ============================================================
FROM node:20-alpine AS production

# Production mode disables source-maps, enables caching
# headers, and silences development warnings in Express.
ENV NODE_ENV=production

WORKDIR /app

# Pull in only the production node_modules from stage 1.
COPY --from=dependencies /app/node_modules ./node_modules

# Copy package manifests (needed by npm start → node src/server.js).
COPY package*.json ./

# Copy application source. The .dockerignore excludes
# node_modules, .env and test files.
COPY src ./src

# Run as the built-in unprivileged user uid 1000 (node) that
# the official Node Alpine image ships with. Use numeric UID
# so the host can always resolve it (Hadolint DL3066).
USER 1000

EXPOSE 3000

# npm start executes: node src/server.js (from package.json).
CMD ["npm", "start"]
