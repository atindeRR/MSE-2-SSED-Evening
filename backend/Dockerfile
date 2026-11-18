
# Use a lightweight Node.js image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package information
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev --no-audit --no-fund

# Copy backend source code
COPY --chown=node:node src ./src

# Run the application as a non-root user
USER node

# Backend listens on port 3000
EXPOSE 3000

# Start the backend server
CMD ["npm", "start"]
