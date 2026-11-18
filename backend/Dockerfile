# Use Node.js on Debian slim
FROM node:22-bookworm-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy backend application code
COPY --chown=node:node . .

# Run as non-root user
USER node

# Backend port
EXPOSE 3000

# Start the backend server
CMD ["npm", "start"]
