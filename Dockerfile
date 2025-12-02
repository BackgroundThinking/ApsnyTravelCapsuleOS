# Multi-stage build for ApsnyTravelCapsuleOS
# Stage 1: Build the application
FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN pnpm build

# Stage 2: Serve the application
FROM node:22-alpine

WORKDIR /app

# Install a simple HTTP server
RUN npm install -g serve

# Copy built application from builder
COPY --from=builder /app/dist/public ./public

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Start the server
CMD ["serve", "-s", "public", "-l", "3000"]
