# =============================================================================
# Backend – Production image
# Node.js Alpine; production dependencies only; no dev tools, no test files.
# The backend/.dockerignore already excludes: node_modules, .env, tests.
# =============================================================================
FROM node:22-alpine

# Set NODE_ENV so any library that branches on it uses production behaviour
ENV NODE_ENV=production

WORKDIR /app

# Copy package.json first for layer caching
COPY package.json ./

# Install only runtime dependencies (no devDependencies).
# No package-lock.json exists in this repo so npm ci is not applicable;
# npm install --omit=dev is used instead.
RUN npm install --omit=dev

# Copy only the application source directory.
# db/ (init.sql) is intentionally excluded – it is consumed by the postgres
# container via /docker-entrypoint-initdb.d/, not by the backend at runtime.
COPY src/ ./src/

EXPOSE 3000

# Production start command (matches the "start" script: node src/server.js).
# Using the exec form directly avoids an npm wrapper process and ensures
# Docker's SIGTERM reaches Node.js for graceful shutdown.
CMD ["node", "src/server.js"]
