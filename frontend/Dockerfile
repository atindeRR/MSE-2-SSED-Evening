
# Stage 1: Build React application
FROM node:20-bookworm-slim AS builder

WORKDIR /app

# Copy package files including package-lock.json
COPY package.json package-lock.json ./

# Install exact locked dependencies
RUN npm ci

# Copy source code
COPY . .

# Build production application
RUN npm run build


# Stage 2: Nginx production server
FROM nginx:alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
