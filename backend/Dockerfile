# Use lightweight official Node.js Alpine base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Copy dependency definition file
COPY package.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy application source code with non-root ownership
COPY --chown=1000:1000 . .

# Run as non-root user (node: uid 1000) for enhanced security
USER 1000

# Expose backend application port
EXPOSE 3000

# Execute server directly so process receives SIGTERM/SIGINT signals
CMD ["node", "src/server.js"]
