
# Stage 1: Build frontend
FROM node:22-alpine AS build

WORKDIR /app

# Copy package files and lockfile
COPY package*.json ./

# Install exact locked dependencies
RUN npm ci

# Copy frontend source
COPY . .

# Build production files
RUN npm run build

# Stage 2: Production Nginx server
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
