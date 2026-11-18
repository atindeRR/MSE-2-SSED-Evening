FROM node:22.22.0-alpine3.23
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev --no-audit --no-fund
COPY --chown=node:node src/ ./src/
USER node
EXPOSE 3000
CMD ["npm", "start"]
