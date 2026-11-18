# Stage 1: Build the React frontend
FROM node:22-alpine AS build

WORKDIR /app

# Copy package files, including the lockfile
COPY package.json package-lock.json ./

# Install exact dependencies
RUN npm ci --no-audit --no-fund

# Copy the frontend source code
COPY . .

# Build the production frontend
RUN npm run build


# Stage 2: Serve frontend using Nginx
FROM nginx:alpine

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]