# ── Backend Dockerfile ──────────────────────────────────────────────
# Uses a slim Node.js image, installs only production dependencies,
# and avoids copying unnecessary files (covered by .dockerignore).

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy dependency manifests first (layer-cache friendly)
COPY package.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source
COPY src/ ./src/
COPY db/  ./db/

# Expose the backend port
EXPOSE 3000

# Start the server
CMD ["node", "src/server.js"]
