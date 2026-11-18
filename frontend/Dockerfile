# ---------- Build Stage ----------
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Install **all** dependencies (dev + prod) because Vite needs devDependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code and build the Vite app
COPY . .
RUN npm run build

# ---------- Production Stage ----------
FROM nginx:stable-alpine

# Copy built static assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Optional custom Nginx configuration (ensure nginx.conf exists in the context)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
