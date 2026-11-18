FROM node:20-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev && addgroup -S appgroup && adduser -S appuser -G appgroup
COPY src/ ./src/
COPY db/ ./db/
EXPOSE 3000
USER appuser
CMD ["node", "src/server.js"]
