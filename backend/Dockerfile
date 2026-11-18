FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# deps first so this layer stays cached when only code changes
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

COPY src ./src

# 1000 = the built-in non-root "node" user (numeric id keeps hadolint DL3066 happy)
USER 1000
EXPOSE 3000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1:3000/health"]
CMD ["node", "src/server.js"]
