
FROM node:20-alpine

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install production dependencies
RUN npm ci --omit=dev

# Copy backend source
COPY src ./src

# Run as non-root user
USER node

EXPOSE 3000

CMD ["npm", "start"]
