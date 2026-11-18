# ── Single-stage production image ──────────────────────────────────────────
FROM node:20-alpine

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy application source
COPY src/ ./src/

ENV NODE_ENV=production

EXPOSE 3000

# Use the package.json "start" script: node src/server.js
CMD ["node", "src/server.js"]
