
# Build stage
FROM node:22-slim AS build

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install exact locked dependencies
RUN npm ci

# Copy frontend source code
COPY . .

# Build production frontend
RUN npm run build

# Production stage
FROM nginx:alpine

# Configure Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only production build files
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
