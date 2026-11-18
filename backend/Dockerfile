# ── Backend Dockerfile ───────────────────────────────────────────────────────
FROM node:20-alpine

# Use non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Install only production dependencies
COPY package.json ./
RUN npm install --omit=dev

# Copy application source (node_modules and .env excluded via .dockerignore)
COPY src/ ./src/
COPY db/  ./db/

# Switch to non-root user
USER appuser

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "src/server.js"]
