# Use lightweight Node.js image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY src/ ./src/

# Use non-root user
USER node

# Expose backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]