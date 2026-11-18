FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies (production only)
COPY package.json .
RUN npm install --production

# Copy source files
COPY . .

# Final image
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app .
EXPOSE 3000
CMD ["npm","run","start"]
