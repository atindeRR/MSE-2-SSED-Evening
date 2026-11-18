
# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY src ./src
COPY db ./db

# Backend port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]
