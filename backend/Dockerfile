# Stage 1: Install production dependencies
FROM node:20-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

# Stage 2: Production runtime
FROM node:20-alpine AS production

ENV NODE_ENV=production
WORKDIR /app

# Copy production dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules
COPY package*.json ./
COPY src ./src

# Run as non-root user (node user UID 1000)
USER 1000:1000

# Expose backend port
EXPOSE 3000

# Start server
CMD ["npm", "start"]
