// ═══════════════════════════════════════════════════════════════════════════
// Redis Cache Layer
// طبقة الكاش باستخدام Redis
//
// Features:
//   - Automatic key generation based on search parameters
//   - Configurable TTL (Time To Live)
//   - Graceful fallback when Redis is unavailable
//   - JSON serialization/deserialization
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"context"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/redis/go-redis/v9"
	"github.com/rs/zerolog/log"
)

const (
	// Cache TTL durations
	CacheTTLShort  = 5 * time.Minute   // للبحث العادي
	CacheTTLMedium = 15 * time.Minute  // للبحث المتشابه
	CacheTTLLong   = 1 * time.Hour     // للاقتراحات

	// Cache key prefixes
	PrefixSearch  = "search:"
	PrefixSimilar = "similar:"
	PrefixSuggest = "suggest:"
)

// ═══════════════════════════════════════════════════════════════════════════
// Redis Connection (اتصال Redis)
// ═══════════════════════════════════════════════════════════════════════════

// connectRedis establishes a connection to Redis
// إنشاء اتصال بـ Redis
func connectRedis(ctx context.Context, redisURL string) (*redis.Client, error) {
	// Parse Redis URL
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		return nil, fmt.Errorf("failed to parse Redis URL: %w", err)
	}

	// تكوين العميل - Configure client
	opts.MaxRetries = 3
	opts.DialTimeout = 5 * time.Second
	opts.ReadTimeout = 3 * time.Second
	opts.WriteTimeout = 3 * time.Second
	opts.PoolSize = 10
	opts.MinIdleConns = 5

	// إنشاء العميل - Create client
	client := redis.NewClient(opts)

	// اختبار الاتصال - Test connection
	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("failed to ping Redis: %w", err)
	}

	return client, nil
}

// ═══════════════════════════════════════════════════════════════════════════
// Cache Operations (عمليات الكاش)
// ═══════════════════════════════════════════════════════════════════════════

// GetFromCache retrieves a value from cache
// استرجاع قيمة من الكاش
func (app *App) GetFromCache(ctx context.Context, key string, result interface{}) (bool, error) {
	if app.Cache == nil {
		return false, nil // Cache not available
	}

	data, err := app.Cache.Get(ctx, key).Bytes()
	if err == redis.Nil {
		return false, nil // Key not found
	}
	if err != nil {
		log.Warn().Err(err).Str("key", key).Msg("Cache get error")
		return false, nil // Graceful fallback
	}

	if err := json.Unmarshal(data, result); err != nil {
		log.Warn().Err(err).Str("key", key).Msg("Cache unmarshal error")
		return false, nil
	}

	log.Debug().Str("key", key).Msg("Cache hit")
	return true, nil
}

// SetToCache stores a value in cache
// تخزين قيمة في الكاش
func (app *App) SetToCache(ctx context.Context, key string, value interface{}, ttl time.Duration) error {
	if app.Cache == nil {
		return nil // Cache not available
	}

	data, err := json.Marshal(value)
	if err != nil {
		return fmt.Errorf("cache marshal error: %w", err)
	}

	if err := app.Cache.Set(ctx, key, data, ttl).Err(); err != nil {
		log.Warn().Err(err).Str("key", key).Msg("Cache set error")
		return nil // Graceful fallback
	}

	log.Debug().Str("key", key).Dur("ttl", ttl).Msg("Cache set")
	return nil
}

// InvalidateCache removes a key from cache
// حذف مفتاح من الكاش
func (app *App) InvalidateCache(ctx context.Context, pattern string) error {
	if app.Cache == nil {
		return nil
	}

	// Get all keys matching pattern
	keys, err := app.Cache.Keys(ctx, pattern).Result()
	if err != nil {
		return err
	}

	if len(keys) == 0 {
		return nil
	}

	// Delete keys
	if err := app.Cache.Del(ctx, keys...).Err(); err != nil {
		return err
	}

	log.Info().Int("count", len(keys)).Str("pattern", pattern).Msg("Cache invalidated")
	return nil
}

// ═══════════════════════════════════════════════════════════════════════════
// Cache Key Generation (إنشاء مفاتيح الكاش)
// ═══════════════════════════════════════════════════════════════════════════

// GenerateCacheKey creates a unique cache key from parameters
// إنشاء مفتاح كاش فريد من المعاملات
func GenerateCacheKey(prefix string, params ...string) string {
	// Join all parameters
	combined := strings.Join(params, "|")

	// Create MD5 hash for shorter keys
	hash := md5.Sum([]byte(combined))
	hashStr := fmt.Sprintf("%x", hash)

	return prefix + hashStr
}

// ═══════════════════════════════════════════════════════════════════════════
// Cache Statistics (إحصائيات الكاش)
// ═══════════════════════════════════════════════════════════════════════════

// CacheStats returns Redis cache statistics
// إحصائيات كاش Redis
func (app *App) CacheStats(ctx context.Context) map[string]interface{} {
	if app.Cache == nil {
		return map[string]interface{}{
			"status": "unavailable",
		}
	}

	stats := app.Cache.PoolStats()
	info := app.Cache.Info(ctx, "stats").Val()

	return map[string]interface{}{
		"status":         "available",
		"hits":           stats.Hits,
		"misses":         stats.Misses,
		"timeouts":       stats.Timeouts,
		"total_conns":    stats.TotalConns,
		"idle_conns":     stats.IdleConns,
		"stale_conns":    stats.StaleConns,
		"server_info":    parseRedisInfo(info),
	}
}

// parseRedisInfo parses Redis INFO command output
func parseRedisInfo(info string) map[string]string {
	result := make(map[string]string)
	lines := strings.Split(info, "\n")

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}

		parts := strings.SplitN(line, ":", 2)
		if len(parts) == 2 {
			result[parts[0]] = parts[1]
		}
	}

	return result
}
