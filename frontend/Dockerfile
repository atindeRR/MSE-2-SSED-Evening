# Stage 1: Build the React application
FROM node:20.18.0-bookworm-slim AS build

# Set working directory for the build stage
WORKDIR /app

# Copy dependency manifests first to leverage layer caching
COPY package*.json ./

# Install all dependencies (including devDependencies required for vite build)
RUN npm install && npm cache clean --force

# Copy application source files
COPY . .

# Build the production artifacts into /app/dist
RUN npm run build

# Stage 2: Serve application using lightweight Nginx
FROM nginx:1.27.2-alpine3.20

# Copy custom Nginx configuration to replace default server block
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static files from build stage to Nginx web root
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]