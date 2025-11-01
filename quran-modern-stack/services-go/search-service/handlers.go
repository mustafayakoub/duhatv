// ═══════════════════════════════════════════════════════════════════════════
// HTTP Handlers
// معالجات HTTP
//
// Endpoints:
//   - GET /health - Health check
//   - GET /metrics - Service metrics
//   - GET /api/search - Search Quran verses
//   - GET /api/similar - Find similar verses
//   - GET /api/suggest - Auto-complete suggestions
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/rs/zerolog/log"
)

// ═══════════════════════════════════════════════════════════════════════════
// Response Helpers (دوال مساعدة للاستجابة)
// ═══════════════════════════════════════════════════════════════════════════

// respondJSON writes a JSON response
// كتابة استجابة JSON
func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)

	if data != nil {
		if err := json.NewEncoder(w).Encode(data); err != nil {
			log.Error().Err(err).Msg("Failed to encode JSON response")
		}
	}
}

// respondError writes an error response
// كتابة استجابة خطأ
func respondError(w http.ResponseWriter, status int, message string) {
	respondJSON(w, status, map[string]interface{}{
		"error":     message,
		"status":    status,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}

// getQueryParam gets a query parameter with a default value
// الحصول على معامل استعلام مع قيمة افتراضية
func getQueryParam(r *http.Request, key, defaultValue string) string {
	value := r.URL.Query().Get(key)
	if value == "" {
		return defaultValue
	}
	return value
}

// getIntParam gets an integer query parameter
// الحصول على معامل استعلام رقمي
func getIntParam(r *http.Request, key string, defaultValue int) int {
	value := r.URL.Query().Get(key)
	if value == "" {
		return defaultValue
	}

	intValue, err := strconv.Atoi(value)
	if err != nil {
		return defaultValue
	}

	return intValue
}

// getFloatParam gets a float query parameter
func getFloatParam(r *http.Request, key string, defaultValue float64) float64 {
	value := r.URL.Query().Get(key)
	if value == "" {
		return defaultValue
	}

	floatValue, err := strconv.ParseFloat(value, 64)
	if err != nil {
		return defaultValue
	}

	return floatValue
}

// ═══════════════════════════════════════════════════════════════════════════
// Health & Metrics Handlers (معالجات الصحة والإحصائيات)
// ═══════════════════════════════════════════════════════════════════════════

// handleHealth returns service health status
// فحص صحة الخدمة
func (app *App) handleHealth(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	// Check database connection
	dbHealthy := true
	if err := app.DB.Ping(ctx); err != nil {
		dbHealthy = false
		log.Error().Err(err).Msg("Database health check failed")
	}

	// Check Redis connection
	redisHealthy := true
	if app.Cache != nil {
		if err := app.Cache.Ping(ctx).Err(); err != nil {
			redisHealthy = false
			log.Warn().Err(err).Msg("Redis health check failed")
		}
	}

	status := "healthy"
	httpStatus := http.StatusOK

	if !dbHealthy {
		status = "unhealthy"
		httpStatus = http.StatusServiceUnavailable
	}

	respondJSON(w, httpStatus, map[string]interface{}{
		"status":    status,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"service":   "quran-search-service",
		"version":   "1.0.0",
		"checks": map[string]bool{
			"database": dbHealthy,
			"redis":    redisHealthy,
		},
	})
}

// handleMetrics returns service metrics
// إحصائيات الخدمة
func (app *App) handleMetrics(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	metrics := map[string]interface{}{
		"timestamp":  time.Now().UTC().Format(time.RFC3339),
		"service":    "quran-search-service",
		"database":   app.DatabaseStats(),
		"cache":      app.CacheStats(ctx),
	}

	respondJSON(w, http.StatusOK, metrics)
}

// ═══════════════════════════════════════════════════════════════════════════
// Search Handlers (معالجات البحث)
// ═══════════════════════════════════════════════════════════════════════════

// handleSearch performs Quran text search
// البحث في نصوص القرآن
//
// Query Parameters:
//   - q: search query (required)
//   - surah: surah number (optional)
//   - juz: juz number (optional)
//   - page: page number (optional)
//   - language: language code (optional, default: ar)
//   - limit: max results (optional, default: 20)
//   - offset: pagination offset (optional, default: 0)
//
// Example: GET /api/search?q=الله&surah=1&limit=10
func (app *App) handleSearch(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	startTime := time.Now()

	// استخراج المعاملات - Extract parameters
	query := getQueryParam(r, "q", "")
	if query == "" {
		respondError(w, http.StatusBadRequest, "Query parameter 'q' is required")
		return
	}

	params := SearchParams{
		Query:    query,
		Surah:    getIntParam(r, "surah", 0),
		Juz:      getIntParam(r, "juz", 0),
		Page:     getIntParam(r, "page", 0),
		Language: getQueryParam(r, "language", "ar"),
		Limit:    getIntParam(r, "limit", 20),
		Offset:   getIntParam(r, "offset", 0),
	}

	// التحقق من صحة المعاملات - Validate parameters
	if params.Limit > 100 {
		params.Limit = 100 // Maximum limit
	}
	if params.Surah < 0 || params.Surah > 114 {
		params.Surah = 0
	}
	if params.Juz < 0 || params.Juz > 30 {
		params.Juz = 0
	}

	// محاولة الحصول من الكاش - Try to get from cache
	cacheKey := GenerateCacheKey(
		PrefixSearch,
		params.Query,
		strconv.Itoa(params.Surah),
		strconv.Itoa(params.Juz),
		strconv.Itoa(params.Page),
		params.Language,
		strconv.Itoa(params.Limit),
		strconv.Itoa(params.Offset),
	)

	var response SearchResponse
	cached, err := app.GetFromCache(ctx, cacheKey, &response)
	if err == nil && cached {
		log.Debug().Str("query", query).Msg("Cache hit for search")
		respondJSON(w, http.StatusOK, response)
		return
	}

	// تنفيذ البحث - Execute search
	results, total, err := app.Search(ctx, params)
	if err != nil {
		log.Error().Err(err).Str("query", query).Msg("Search failed")
		respondError(w, http.StatusInternalServerError, "Search failed")
		return
	}

	// بناء الاستجابة - Build response
	executionTime := time.Since(startTime).Milliseconds()
	response = SearchResponse{
		Results:         results,
		Total:           total,
		Query:           params.Query,
		Limit:           params.Limit,
		Offset:          params.Offset,
		ExecutionTimeMS: float64(executionTime),
	}

	// حفظ في الكاش - Save to cache
	_ = app.SetToCache(ctx, cacheKey, response, CacheTTLShort)

	log.Info().
		Str("query", query).
		Int("results", len(results)).
		Int("total", total).
		Int64("duration_ms", executionTime).
		Msg("Search completed")

	respondJSON(w, http.StatusOK, response)
}

// ═══════════════════════════════════════════════════════════════════════════
// Similar Search Handler (معالج البحث عن المتشابهات)
// ═══════════════════════════════════════════════════════════════════════════

// handleSimilar finds similar verses
// البحث عن آيات مشابهة
//
// Query Parameters:
//   - text: text to find similar verses (required)
//   - threshold: similarity threshold 0-1 (optional, default: 0.3)
//   - limit: max results (optional, default: 10)
//
// Example: GET /api/similar?text=بسم الله الرحمن الرحيم&threshold=0.5
func (app *App) handleSimilar(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	startTime := time.Now()

	// استخراج المعاملات - Extract parameters
	text := getQueryParam(r, "text", "")
	if text == "" {
		respondError(w, http.StatusBadRequest, "Query parameter 'text' is required")
		return
	}

	params := SimilarParams{
		Text:      text,
		Threshold: getFloatParam(r, "threshold", 0.3),
		Limit:     getIntParam(r, "limit", 10),
	}

	// التحقق من صحة المعاملات - Validate parameters
	if params.Threshold < 0 || params.Threshold > 1 {
		params.Threshold = 0.3
	}
	if params.Limit > 50 {
		params.Limit = 50
	}

	// محاولة الحصول من الكاش - Try cache
	cacheKey := GenerateCacheKey(
		PrefixSimilar,
		params.Text,
		strconv.FormatFloat(params.Threshold, 'f', 2, 64),
		strconv.Itoa(params.Limit),
	)

	var results []SearchResult
	cached, err := app.GetFromCache(ctx, cacheKey, &results)
	if err == nil && cached {
		respondJSON(w, http.StatusOK, map[string]interface{}{
			"results":          results,
			"total":            len(results),
			"text":             params.Text,
			"threshold":        params.Threshold,
			"execution_time_ms": time.Since(startTime).Milliseconds(),
		})
		return
	}

	// تنفيذ البحث - Execute search
	results, err = app.FindSimilar(ctx, params)
	if err != nil {
		log.Error().Err(err).Str("text", text).Msg("Similar search failed")
		respondError(w, http.StatusInternalServerError, "Similar search failed")
		return
	}

	// حفظ في الكاش - Save to cache
	_ = app.SetToCache(ctx, cacheKey, results, CacheTTLMedium)

	log.Info().
		Str("text", text).
		Int("results", len(results)).
		Float64("threshold", params.Threshold).
		Msg("Similar search completed")

	respondJSON(w, http.StatusOK, map[string]interface{}{
		"results":          results,
		"total":            len(results),
		"text":             params.Text,
		"threshold":        params.Threshold,
		"execution_time_ms": time.Since(startTime).Milliseconds(),
	})
}

// ═══════════════════════════════════════════════════════════════════════════
// Auto-complete Handler (معالج الإكمال التلقائي)
// ═══════════════════════════════════════════════════════════════════════════

// handleSuggest provides auto-complete suggestions
// اقتراحات الإكمال التلقائي
//
// Query Parameters:
//   - q: partial query (required)
//   - limit: max suggestions (optional, default: 5)
//
// Example: GET /api/suggest?q=الفات
func (app *App) handleSuggest(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	// استخراج المعاملات - Extract parameters
	query := getQueryParam(r, "q", "")
	if query == "" || len(query) < 2 {
		respondError(w, http.StatusBadRequest, "Query parameter 'q' must be at least 2 characters")
		return
	}

	limit := getIntParam(r, "limit", 5)
	if limit > 20 {
		limit = 20
	}

	// محاولة الحصول من الكاش - Try cache
	cacheKey := GenerateCacheKey(PrefixSuggest, query, strconv.Itoa(limit))

	var suggestions []Suggestion
	cached, err := app.GetFromCache(ctx, cacheKey, &suggestions)
	if err == nil && cached {
		respondJSON(w, http.StatusOK, map[string]interface{}{
			"suggestions": suggestions,
			"query":       query,
		})
		return
	}

	// الحصول على الاقتراحات - Get suggestions
	suggestions, err = app.GetSuggestions(ctx, query, limit)
	if err != nil {
		log.Error().Err(err).Str("query", query).Msg("Suggestions failed")
		respondError(w, http.StatusInternalServerError, "Suggestions failed")
		return
	}

	// حفظ في الكاش - Save to cache
	_ = app.SetToCache(ctx, cacheKey, suggestions, CacheTTLLong)

	respondJSON(w, http.StatusOK, map[string]interface{}{
		"suggestions": suggestions,
		"query":       query,
	})
}
