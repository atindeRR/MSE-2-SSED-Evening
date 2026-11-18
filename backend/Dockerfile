
# Use lightweight Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy dependency information
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev && npm cache clean --force

# Copy application source code
COPY --chown=node:node src ./src

# Run as non-root user
USER node

# Backend application port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]
