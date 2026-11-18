# Use Node.js LTS Alpine for a lightweight production image
FROM node:22-alpine

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --omit=dev --no-audit --no-fund

# Copy only application source code
COPY --chown=node:node src ./src

# Run the application as a non-root user
USER node

EXPOSE 3000

# Check backend and its PostgreSQL/Redis dependencies
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3000/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["npm", "start"]
