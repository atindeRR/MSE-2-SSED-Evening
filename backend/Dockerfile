# Production Node.js runtime
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Configure production environment
ENV NODE_ENV=production

# Copy dependency specifications
COPY package*.json ./

# Install production dependencies only (respects lockfile if present)
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --omit=dev; fi

# Copy backend source code and database initialization schema
COPY src/ ./src/
COPY db/ ./db/

# Expose backend application port
EXPOSE 3000

# Start backend server
CMD ["node", "src/server.js"]
