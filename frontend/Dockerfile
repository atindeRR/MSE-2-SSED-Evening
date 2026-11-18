# Stage 1: Build React application
FROM node:20 AS builder

WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install dependencies using lockfile
RUN npm ci

# Copy frontend source code
COPY . .

# Create production build
RUN npm run build

# Stage 2: Production using Nginx
FROM nginx:alpine

# Copy production build files
COPY --from=builder /app/dist /usr/share/nginx/html

# Configure Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose frontend port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
