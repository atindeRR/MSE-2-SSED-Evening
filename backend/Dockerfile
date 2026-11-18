# Production-optimised backend image
FROM node:20-alpine

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Install only production dependencies
COPY package.json ./
RUN npm install --omit=dev

# Copy application source
COPY src/ ./src/

# Drop to non-root user
USER appuser

EXPOSE 3000

CMD ["node", "src/server.js"]
