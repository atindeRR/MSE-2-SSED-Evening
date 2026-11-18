
# Use a lightweight Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency manifests
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY src ./src

# Backend listens on port 3000
EXPOSE 3000

# Start the backend server
CMD ["npm", "start"]
