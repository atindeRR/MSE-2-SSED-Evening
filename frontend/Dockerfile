# Stage 1: Build the React frontend using Node.js (slim uses glibc for Vite/Rollup)
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code and build production files
COPY . .
RUN npm run build

# Stage 2: Serve static files using lightweight Nginx
FROM nginx:1.27-alpine

# Remove default Nginx configuration and copy custom nginx.conf
RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the compiled production artifacts from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port 80
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]