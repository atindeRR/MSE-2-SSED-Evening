
# Use Node.js base image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Production environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source
COPY src ./src
COPY db ./db

# Backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
