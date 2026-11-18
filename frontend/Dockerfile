# Stage 1: Build React application
FROM node:24-alpine AS builder
WORKDIR /app
# Copy dependency files
COPY package.json package-lock.json ./
# Install exact locked dependencies
RUN npm ci
# Copy frontend source code
COPY . .
# Build production application
RUN npm run build
# Stage 2: Serve using Nginx
FROM nginx:alpine
# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf
# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy only production build files
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

