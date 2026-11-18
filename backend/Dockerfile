
FROM node:20-alpine

WORKDIR /app

# Copy package configuration
COPY package.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source
COPY src ./src

# Run as non-root user
USER node

EXPOSE 3000

CMD ["npm", "start"]

