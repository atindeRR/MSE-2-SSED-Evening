
# Use Node.js production image
FROM node:26-bookworm-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm ci --omit=dev

# Copy backend source code
COPY . .

# Set production environment
ENV NODE_ENV=production

# Backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
