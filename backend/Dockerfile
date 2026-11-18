# ---------------------------------------------------------------
# TaskFlow backend (Express API) - production image
# ---------------------------------------------------------------
FROM node:22-alpine

# Production mode: Express disables verbose errors, npm skips devDependencies
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# 1) Copy only the dependency manifests first so this layer is cached
#    and "npm ci" re-runs only when dependencies actually change.
COPY package.json package-lock.json ./

# 2) Install ONLY production dependencies, reproducibly from the lockfile,
#    and drop the npm cache so it does not bloat the image.
RUN npm ci --omit=dev && npm cache clean --force

# 3) Copy only the application source code
#    (tests, .env, node_modules etc. are excluded by .dockerignore).
COPY --chown=1000:1000 src ./src

# Run as the unprivileged "node" user (uid 1000) that ships with the official image
USER 1000:1000

EXPOSE 3000

# Container-level health check: /health verifies PostgreSQL and Redis too
HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]

CMD ["node", "src/server.js"]
