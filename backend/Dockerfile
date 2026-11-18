
# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy backend source code
COPY src ./src
COPY db ./db

# Expose backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]

