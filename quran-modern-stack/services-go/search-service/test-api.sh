#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# Quran Search Service - API Testing Script
# سكريبت اختبار واجهة برمجة التطبيقات
#
# Usage: ./test-api.sh
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${BASE_URL:-http://localhost:8001}"
VERBOSE="${VERBOSE:-false}"

# ───────────────────────────────────────────────────────────────────────────
# Helper Functions
# ───────────────────────────────────────────────────────────────────────────

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}\n"
}

print_test() {
    echo -e "${YELLOW}▶ Testing:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓ Success:${NC} $1"
}

print_error() {
    echo -e "${RED}✗ Error:${NC} $1"
}

# ───────────────────────────────────────────────────────────────────────────
# Test Functions
# ───────────────────────────────────────────────────────────────────────────

test_health() {
    print_test "Health Check"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/health")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        print_success "Service is healthy"
        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq .
        fi
    else
        print_error "Service is unhealthy (HTTP $http_code)"
        echo "$body"
        return 1
    fi
}

test_metrics() {
    print_test "Metrics Endpoint"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/metrics")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        print_success "Metrics retrieved"
        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq .
        fi
    else
        print_error "Failed to get metrics (HTTP $http_code)"
        return 1
    fi
}

test_search_simple() {
    print_test "Simple Search - الله"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/search?q=الله&limit=5")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        total=$(echo "$body" | jq -r '.total')
        results_count=$(echo "$body" | jq -r '.results | length')
        exec_time=$(echo "$body" | jq -r '.execution_time_ms')

        print_success "Found $total results, returned $results_count in ${exec_time}ms"

        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq '.results[0]'
        fi
    else
        print_error "Search failed (HTTP $http_code)"
        echo "$body"
        return 1
    fi
}

test_search_with_filters() {
    print_test "Search with Filters - الله in Surah 1"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/search?q=الله&surah=1&limit=10")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        total=$(echo "$body" | jq -r '.total')
        print_success "Found $total results in Surah 1"

        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq '.results[] | {surah: .surah_number, ayah: .ayah_number, text: .text_simple}'
        fi
    else
        print_error "Filtered search failed (HTTP $http_code)"
        return 1
    fi
}

test_similar() {
    print_test "Similar Verses - بسم الله الرحمن الرحيم"

    text="بسم الله الرحمن الرحيم"
    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/similar?text=$text&threshold=0.3&limit=5")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        total=$(echo "$body" | jq -r '.total')
        print_success "Found $total similar verses"

        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq '.results[] | {rank: .rank, text: .text_simple}'
        fi
    else
        print_error "Similar search failed (HTTP $http_code)"
        return 1
    fi
}

test_suggest() {
    print_test "Auto-complete Suggestions - الفات"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/suggest?q=الفات&limit=5")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        count=$(echo "$body" | jq -r '.suggestions | length')
        print_success "Found $count suggestions"

        if [ "$VERBOSE" = "true" ]; then
            echo "$body" | jq '.suggestions'
        fi
    else
        print_error "Suggestions failed (HTTP $http_code)"
        return 1
    fi
}

test_error_handling() {
    print_test "Error Handling - Empty Query"

    response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/search?q=")
    http_code=$(echo "$response" | tail -n 1)

    if [ "$http_code" = "400" ]; then
        print_success "Correctly returned 400 for empty query"
    else
        print_error "Expected 400, got $http_code"
        return 1
    fi
}

# ───────────────────────────────────────────────────────────────────────────
# Main Test Suite
# ───────────────────────────────────────────────────────────────────────────

main() {
    print_header "🔍 Quran Search Service - API Tests"

    echo "Testing against: $BASE_URL"
    echo "Verbose mode: $VERBOSE"
    echo ""

    # Check if service is running
    if ! curl -s "$BASE_URL/health" > /dev/null 2>&1; then
        print_error "Service is not running at $BASE_URL"
        echo "Start the service with: make dev"
        exit 1
    fi

    # Run tests
    test_health || exit 1
    test_metrics || exit 1
    test_search_simple || exit 1
    test_search_with_filters || exit 1
    test_similar || exit 1
    test_suggest || exit 1
    test_error_handling || exit 1

    print_header "✅ All Tests Passed!"

    echo ""
    echo "Additional manual tests:"
    echo "  curl '$BASE_URL/api/search?q=الرحمن&limit=10' | jq"
    echo "  curl '$BASE_URL/api/similar?text=قل هو الله أحد&threshold=0.5' | jq"
    echo "  curl '$BASE_URL/api/suggest?q=الب' | jq"
    echo ""
}

# Run main function
main "$@"
