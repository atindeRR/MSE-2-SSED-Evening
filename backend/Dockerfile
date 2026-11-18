FROM node:18-alpine AS base

# Set working directory
WORKDIR /app

# Install production dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Copy application source
COPY src/ ./src

# Expose the port the server runs on (default 3000)
EXPOSE 3000

# Start the server
CMD ["node", "src/server.js"]

