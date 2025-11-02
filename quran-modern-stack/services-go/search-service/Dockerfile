# ═══════════════════════════════════════════════════════════════════════════
# Quran Modern Stack - Go Search Service Dockerfile
# Multi-stage build for optimized production image
# ═══════════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────────────
# Stage 1: Builder (مرحلة البناء)
# ───────────────────────────────────────────────────────────────────────────
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git ca-certificates tzdata

# Set working directory
WORKDIR /build

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download && go mod verify

# Copy source code
COPY . .

# Build the application
# CGO_ENABLED=0 for static binary
# -ldflags for smaller binary size
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags='-w -s -extldflags "-static"' \
    -o /app/search-service \
    .

# ───────────────────────────────────────────────────────────────────────────
# Stage 2: Runtime (مرحلة التشغيل)
# ───────────────────────────────────────────────────────────────────────────
FROM scratch

# Copy CA certificates from builder
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy timezone data
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Copy the binary
COPY --from=builder /app/search-service /app/search-service

# Expose port
EXPOSE 8001

# Set user (non-root)
USER 1000:1000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["/app/search-service", "--health-check"]

# Run the application
ENTRYPOINT ["/app/search-service"]

# ═══════════════════════════════════════════════════════════════════════════
# Build instructions:
#
# Build image:
#   docker build -t quran-search-service:latest .
#
# Run container:
#   docker run -p 8001:8001 \
#     -e DATABASE_URL=postgresql://... \
#     -e REDIS_URL=redis://... \
#     quran-search-service:latest
#
# Multi-platform build:
#   docker buildx build --platform linux/amd64,linux/arm64 \
#     -t quran-search-service:latest .
# ═══════════════════════════════════════════════════════════════════════════
