
FROM node:22-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy backend source code
COPY src ./src

# Expose backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
