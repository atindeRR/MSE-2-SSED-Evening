
# Stage 1: Build React application
FROM node:20-bookworm-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --include=dev --ignore-scripts=false

COPY . .

RUN npm run build

# Stage 2: Production server
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
