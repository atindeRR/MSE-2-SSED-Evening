
# Use Node.js 22 lightweight image
FROM node:22-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY src ./src

# Copy database initialization script
COPY db ./db

# Backend listens on port 3000
EXPOSE 3000

# Start the backend application
CMD ["npm", "start"]
