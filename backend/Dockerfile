FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

# Install production dependencies as root, then run the app as non-root.
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

# Copy only runtime source files and give them to the node user.
COPY --chown=node:node src/ ./src/

EXPOSE 3000

USER node

CMD ["npm", "start"]