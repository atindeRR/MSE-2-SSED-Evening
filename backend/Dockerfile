
# Use lightweight Node.js image
FROM node:22-alpine

WORKDIR /app

# Copy dependency information
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY src ./src

# Application port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
