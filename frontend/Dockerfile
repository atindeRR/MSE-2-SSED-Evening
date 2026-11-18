# Stage 1: Build React application
FROM node:22-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install exact locked dependencies
RUN npm ci

# Copy frontend source
COPY . .

# Build production application
RUN npm run build

# Stage 2: Production Nginx server
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]