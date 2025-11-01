# ═══════════════════════════════════════════════════════════════════════════
# Quran Modern Stack - Rust Backend Dockerfile
# Multi-stage build for optimized production image
# ═══════════════════════════════════════════════════════════════════════════

# Stage 1: Build
FROM rust:1.75-alpine AS builder

# Install dependencies
RUN apk add --no-cache musl-dev openssl-dev

WORKDIR /app

# Copy manifests
COPY Cargo.toml ./

# Copy source code
COPY src ./src

# Build release binary
RUN cargo build --release

# Stage 2: Runtime
FROM alpine:latest

RUN apk add --no-cache libgcc

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/target/release/quran-backend-rust ./quran-backend-rust

# Expose port
EXPOSE 8000

# Run
CMD ["./quran-backend-rust"]
