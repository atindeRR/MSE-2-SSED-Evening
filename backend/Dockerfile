# Use Node.js 20 Alpine for a small production image
FROM node:20-alpine

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package files first for layer caching
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy only the application source (no tests, no docs, no unnecessary files)
COPY src ./src

EXPOSE 3000

CMD ["node", "src/server.js"]
