
# Use Node.js lightweight image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application files
COPY . .

# Use production environment
ENV NODE_ENV=production

# Backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
