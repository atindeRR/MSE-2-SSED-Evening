# ---------- Stage 1: build the React app ----------
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
# No lockfile in repo, so npm picks the newest rollup; rollup 4.68.x musl binary
# crashes on Alpine ("Code is nested too deeply"). Pin a known-good rollup.
RUN npm install && npm install --no-save rollup@4.40.0

COPY . .
RUN npm run build

# ---------- Stage 2: serve static files with nginx ----------
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD ["wget", "-qO-", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
