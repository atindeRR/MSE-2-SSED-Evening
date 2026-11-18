
FROM node:22-alpine

WORKDIR /app

# Copy package information
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev --no-audit --no-fund

# Copy backend source code
COPY src ./src

# Create non-root user
USER node

EXPOSE 3000

CMD ["npm", "start"]
