
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source
COPY src ./src

# Set production environment
ENV NODE_ENV=production

# Backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]
