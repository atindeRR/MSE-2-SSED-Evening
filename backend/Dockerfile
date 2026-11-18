FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

# Copy only manifests first so the dependency layer is cached until package*.json changes
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Only the runtime source; db/init.sql is mounted into postgres, not needed here
COPY src ./src

# run as the non-root "node" user (uid 1000) that ships with the image
USER 1000
EXPOSE 3000
CMD ["node", "src/server.js"]
