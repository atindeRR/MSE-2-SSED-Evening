# ---------------------------------------------------------------
# TaskFlow backend (Express API) - production image
# ---------------------------------------------------------------
FROM node:20-alpine

# Set production environment variables
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# Install production dependencies only using package-lock.json
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy only source files
COPY --chown=node:node src ./src

# Run as non-root user
USER node

EXPOSE 3000

# Health check to verify backend API health
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:' + (process.env.PORT || 3000) + '/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
