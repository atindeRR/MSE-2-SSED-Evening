# Stage 1: Build React application
FROM node:22-bookworm-slim AS build
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci
RUN npm ls vite rollup react react-dom
# Copy application source
COPY . .

# Build React application
RUN npm run build


# Stage 2: Nginx production server
FROM nginx:alpine

# Remove default Nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy React build output
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
