FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

COPY src ./src

# "node" user (uid 1000) is built into the official node image
# hadolint ignore=DL3066
USER node

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD ["wget", "-qO-", "http://127.0.0.1:3000/health"]

CMD ["node", "src/server.js"]
