# syntax=docker/dockerfile:1

FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY src ./src
RUN addgroup -S -g 1001 appgroup \
    && adduser -S -u 1001 -G appgroup appuser \
    && chown -R appuser:appgroup /app
USER 1001
EXPOSE 3000
CMD ["node", "src/server.js"]

