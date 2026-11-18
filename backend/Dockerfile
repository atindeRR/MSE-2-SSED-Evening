FROM node:20-alpine

# Set production environment
ENV NODE_ENV=production

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY src ./src

# Expose backend API port
EXPOSE 3000

# Run as non-root node user for better security
USER node

# Start the Express server
CMD ["node", "src/server.js"]