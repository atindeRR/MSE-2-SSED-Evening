
# Use lightweight Node.js image
FROM node:24-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy backend source code
COPY src ./src

# Expose backend port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]
