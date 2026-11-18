FROM node:22-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev --no-audit --no-fund && npm cache clean --force

COPY --chown=1000:1000 src ./src
COPY --chown=1000:1000 db ./db
USER 1000:1000

EXPOSE 3000
# hadolint ignore=DL3025
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 CMD ["node", "-e", "fetch('http://127.0.0.1:3000/health').then((r) => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
