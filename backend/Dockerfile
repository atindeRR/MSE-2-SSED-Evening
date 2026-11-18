FROM node:20-alpine

# Set working directory
WORKDIR /app

# Configure production environment
ENV NODE_ENV=production

# Copy dependency definition files
COPY package*.json ./

# Install only production dependencies and clean cache
RUN npm install --omit=dev && npm cache clean --force

# Copy application source code with non-root ownership
COPY --chown=node:node . .

# Run as non-root user (UID 1000 for node user)
USER 1000:1000

# Expose backend application port
EXPOSE 3000

# Start backend application
CMD ["node", "src/server.js"]
