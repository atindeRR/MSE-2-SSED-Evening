# ==========================================
# Backend Production Dockerfile
# ==========================================

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Set production environment variable
ENV NODE_ENV=production
ENV PORT=5000

# Install curl/wget for healthcheck if needed
RUN apk add --no-cache curl

# Copy dependency manifests
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production || npm install --omit=dev --production

# Copy backend application source code
COPY . .

# Expose backend application port
EXPOSE 5000

# Health check to verify backend server is responding
HEALTHCHECK --interval=15s --timeout=5s --retries=5 --start-period=15s \
  CMD curl -f http://localhost:5000/health || wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1

# Start the application
CMD ["npm", "start"]
