FROM node:24-alpine

ENV NODE_ENV=production

WORKDIR /app

COPY --chown=node:node package.json package-lock.json ./

RUN npm ci --omit=dev

COPY --chown=node:node src ./src

USER 1000:1000

EXPOSE 3000

CMD ["node", "src/server.js"]
