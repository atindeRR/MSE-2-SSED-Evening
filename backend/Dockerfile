FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

COPY package*.json ./
RUN npm install --omit=dev

COPY --chown=1000:1000 src/ ./src/
COPY --chown=1000:1000 db/ ./db/

USER 1000

EXPOSE 3000

CMD ["npm", "start"]
