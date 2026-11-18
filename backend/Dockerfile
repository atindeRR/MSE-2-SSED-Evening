# Multi-stage build for Node.js Express backend application

# Stage 1: Install production dependencies
FROM node:20-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

# Stage 2: Production runtime environment
FROM node:20-alpine AS production

ENV NODE_ENV=production
WORKDIR /app

# Copy dependencies and application source with non-root ownership
COPY --from=dependencies --chown=1000:1000 /app/node_modules ./node_modules
COPY --chown=1000:1000 package*.json ./
COPY --chown=1000:1000 src ./src

# Run as non-root user (node user: UID 1000, GID 1000)
USER 1000:1000

# Expose backend application port
EXPOSE 3000

# Health check to verify API responsiveness
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=15s \
  CMD ["node", "-e", "fetch('http://127.0.0.1:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]

CMD ["npm", "start"]