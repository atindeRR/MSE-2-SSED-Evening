# Stage 1: Dependency resolution stage
FROM node:20-alpine AS dependencies

WORKDIR /app

# Copy dependency manifests
COPY package*.json ./

# Install production dependencies only and clear npm cache
RUN npm install --omit=dev && npm cache clean --force

# Stage 2: Production runtime stage
FROM node:20-alpine AS production

ENV NODE_ENV=production
WORKDIR /app

# Copy production node_modules from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy application configuration and source files
COPY package*.json ./
COPY src ./src

# Run as non-root user for security
USER node

# Expose backend application port
EXPOSE 3000

# Start server directly with Node.js
CMD ["node", "src/server.js"]
