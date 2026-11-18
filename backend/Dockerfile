FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

COPY src ./src
COPY db ./db

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "src/server.js"]
