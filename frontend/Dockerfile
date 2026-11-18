# Stage 1: Build the React/Vite application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency definition first (leverages Docker layer cache)
COPY package.json ./

# Install all dependencies (including devDependencies needed for Vite build)
# Using npm install because no package-lock.json exists in this repository
RUN npm install

# Copy application source code
COPY . .

# Build production bundle (outputs to /app/dist)
RUN npm run build

# Stage 2: Serve with lightweight Nginx
FROM nginx:1.27-alpine

# Copy custom Nginx config (reverse proxy + SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the production build artifacts from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Nginx runs in foreground
CMD ["nginx", "-g", "daemon off;"]
