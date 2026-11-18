# Stage 1: Build React application
FROM node:22-slim AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install --no-audit --no-fund \
    && npm cache clean --force

COPY . .

RUN npm run build

# Stage 2: Production runtime with Nginx
FROM nginx:1.27-alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
