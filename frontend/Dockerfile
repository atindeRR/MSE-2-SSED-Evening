# ---------- Stage 1: build React app with Node ----------
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ---------- Stage 2: serve static files with Nginx ----------
FROM nginx:1.27-alpine
# Replace default config with ours (it proxies /api -> backend:3000)
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy ONLY the built files, no node_modules / source code
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
