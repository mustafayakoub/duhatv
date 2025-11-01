# ═══════════════════════════════════════════════════════════════════════════
# Quran Search Service - Makefile
# خدمة البحث في القرآن - ملف Make
# ═══════════════════════════════════════════════════════════════════════════

.PHONY: help build run test clean docker-build docker-run install dev lint

# ───────────────────────────────────────────────────────────────────────────
# Variables
# ───────────────────────────────────────────────────────────────────────────
BINARY_NAME=search-service
DOCKER_IMAGE=quran-search-service
DOCKER_TAG=latest
GO=go

# ───────────────────────────────────────────────────────────────────────────
# Help
# ───────────────────────────────────────────────────────────────────────────
help: ## Show this help message
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "Quran Search Service - Makefile Commands"
	@echo "خدمة البحث في القرآن - أوامر Make"
	@echo "═══════════════════════════════════════════════════════════════════"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "═══════════════════════════════════════════════════════════════════"

# ───────────────────────────────────────────────────────────────────────────
# Development
# ───────────────────────────────────────────────────────────────────────────
install: ## Install dependencies
	@echo "📦 Installing dependencies..."
	$(GO) mod download
	$(GO) mod verify
	@echo "✅ Dependencies installed"

dev: ## Run in development mode with auto-reload
	@echo "🚀 Starting development server..."
	$(GO) run .

run: build ## Build and run the application
	@echo "🚀 Running $(BINARY_NAME)..."
	./$(BINARY_NAME)

build: ## Build the application
	@echo "🔨 Building $(BINARY_NAME)..."
	$(GO) build -o $(BINARY_NAME) .
	@echo "✅ Build complete: $(BINARY_NAME)"

# ───────────────────────────────────────────────────────────────────────────
# Testing & Quality
# ───────────────────────────────────────────────────────────────────────────
test: ## Run tests
	@echo "🧪 Running tests..."
	$(GO) test -v ./...

test-cover: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	$(GO) test -cover -coverprofile=coverage.out ./...
	$(GO) tool cover -html=coverage.out -o coverage.html
	@echo "✅ Coverage report generated: coverage.html"

bench: ## Run benchmarks
	@echo "⚡ Running benchmarks..."
	$(GO) test -bench=. -benchmem ./...

lint: ## Run linter
	@echo "🔍 Running linter..."
	golangci-lint run ./...

fmt: ## Format code
	@echo "✨ Formatting code..."
	$(GO) fmt ./...
	gofmt -s -w .

vet: ## Run go vet
	@echo "🔍 Running go vet..."
	$(GO) vet ./...

# ───────────────────────────────────────────────────────────────────────────
# Docker
# ───────────────────────────────────────────────────────────────────────────
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "✅ Docker image built: $(DOCKER_IMAGE):$(DOCKER_TAG)"

docker-run: ## Run Docker container
	@echo "🐳 Running Docker container..."
	docker run -p 8001:8001 \
		-e DATABASE_URL=${DATABASE_URL} \
		-e REDIS_URL=${REDIS_URL} \
		$(DOCKER_IMAGE):$(DOCKER_TAG)

docker-push: docker-build ## Build and push Docker image
	@echo "🐳 Pushing Docker image..."
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)

# ───────────────────────────────────────────────────────────────────────────
# Utilities
# ───────────────────────────────────────────────────────────────────────────
clean: ## Clean build artifacts
	@echo "🧹 Cleaning..."
	rm -f $(BINARY_NAME)
	rm -f coverage.out coverage.html
	$(GO) clean
	@echo "✅ Clean complete"

tidy: ## Tidy go.mod
	@echo "🧹 Tidying go.mod..."
	$(GO) mod tidy
	@echo "✅ go.mod tidied"

update: ## Update dependencies
	@echo "📦 Updating dependencies..."
	$(GO) get -u ./...
	$(GO) mod tidy
	@echo "✅ Dependencies updated"

# ───────────────────────────────────────────────────────────────────────────
# Production
# ───────────────────────────────────────────────────────────────────────────
build-prod: ## Build for production
	@echo "🔨 Building for production..."
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 $(GO) build \
		-ldflags='-w -s -extldflags "-static"' \
		-o $(BINARY_NAME) .
	@echo "✅ Production build complete"

# ───────────────────────────────────────────────────────────────────────────
# Database
# ───────────────────────────────────────────────────────────────────────────
db-test: ## Test database connection
	@echo "🔌 Testing database connection..."
	psql $(DATABASE_URL) -c "SELECT version();"

# ───────────────────────────────────────────────────────────────────────────
# Default
# ───────────────────────────────────────────────────────────────────────────
.DEFAULT_GOAL := help
