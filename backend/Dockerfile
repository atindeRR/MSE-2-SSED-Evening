# Use an appropriate lightweight, pinned Node.js LTS base image
FROM node:20.18.0-alpine3.20

# Set production environment
ENV NODE_ENV=production

# Set the working directory inside the container
WORKDIR /app

# Copy dependency manifests first to leverage Docker layer caching
COPY --chown=node:node package*.json ./

# Install production dependencies only and clear the npm cache
RUN npm install --omit=dev && npm cache clean --force

# Copy only the required backend application source files
COPY --chown=node:node src/ ./src/

# Run the application as a non-root user
USER node

# Expose the application port (defaults to 3000 in server.js / config.js)
EXPOSE 3000

# Default command to start the backend application
CMD ["npm", "start"]