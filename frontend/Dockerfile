
# Stage 1: Build React application
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

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
