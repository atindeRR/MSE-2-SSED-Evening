# Production backend image
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Copy dependency definition
COPY package.json ./

# Install production dependencies only
# Using npm install because no package-lock.json exists in this repository
RUN npm install --omit=dev

# Copy application source and database init script
COPY src/ ./src/
COPY db/ ./db/

# Switch to non-root user by numeric UID:GID (Hadolint DL3066 best practice)
USER 1000:1000

# Expose the API port
EXPOSE 3000

# Start the Express server
CMD ["npm", "start"]
