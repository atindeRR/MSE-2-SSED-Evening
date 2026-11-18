FROM node:20-slim AS builder
WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source files
COPY . .

# Build the frontend
RUN npm run build

# Production image
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

