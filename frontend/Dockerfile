
# Stage 1: Build React application
FROM node:20-slim AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source code
COPY . .

# Build production application
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

# Copy production build to Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose Nginx port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
