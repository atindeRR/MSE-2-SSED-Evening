# ---------- Backend: production-oriented Node.js image ----------
FROM node:20-alpine

# Production mode: Express disables verbose errors, npm skips dev tooling
ENV NODE_ENV=production

WORKDIR /app

# Copy only the manifest first so the dependency layer is cached
# until package.json actually changes
COPY package.json ./

# Install only runtime dependencies (no lock file exists in the repo, so npm ci cannot be used)
RUN npm install --omit=dev && npm cache clean --force

# Copy only the application source (db/init.sql is mounted into PostgreSQL by Compose,
# tests and .env are excluded by .dockerignore)
COPY src ./src

# Run as the unprivileged user that ships with the official Node image
USER node

EXPOSE 3000

CMD ["node", "src/server.js"]
