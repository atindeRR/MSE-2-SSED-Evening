
# Use lightweight Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency configuration
COPY package.json ./

# Install production dependencies only
RUN npm install --omit=dev --no-audit --no-fund

# Copy backend source code
COPY src ./src

# Run as non-root user
USER node

# Backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
