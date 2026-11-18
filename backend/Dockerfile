# ---------- Backend: production Node.js image ----------
FROM node:20-alpine

# Production mode: express etc. optimise themselves, npm skips devDependencies
ENV NODE_ENV=production
WORKDIR /app

# 1) Copy ONLY package files first -> dependency layer cache hota hai
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

# 2) Copy only application source (node_modules, .env, tests .dockerignore se bahar)
COPY src ./src

# 3) Run as non-root user (node user is built into the image)
USER node

EXPOSE 3000

# Container-level health check (wget is present in alpine/busybox)
HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1

CMD ["node", "src/server.js"]
