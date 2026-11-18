# Production-oriented Node.js runtime
FROM node:20-alpine

WORKDIR /app

# Production environment configuration
ENV NODE_ENV=production

# Copy package manifests
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Expose backend application port
EXPOSE 3000

# Start backend application
CMD ["node", "src/server.js"]
