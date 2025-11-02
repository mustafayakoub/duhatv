// ═══════════════════════════════════════════════════════════════════════════
// Database Connection & Utilities
// الاتصال بقاعدة البيانات والأدوات المساعدة
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

// connectDB establishes a connection pool to PostgreSQL
// إنشاء مجموعة اتصالات بـ PostgreSQL
func connectDB(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	// Parse connection string
	config, err := pgxpool.ParseConfig(databaseURL)
	if err != nil {
		return nil, fmt.Errorf("failed to parse database URL: %w", err)
	}

	// تكوين مجموعة الاتصالات - Configure connection pool
	config.MaxConns = 25                          // الحد الأقصى للاتصالات
	config.MinConns = 5                           // الحد الأدنى للاتصالات
	config.MaxConnLifetime = time.Hour            // عمر الاتصال الأقصى
	config.MaxConnIdleTime = 30 * time.Minute     // وقت الخمول الأقصى
	config.HealthCheckPeriod = 1 * time.Minute    // فترة فحص الصحة

	// إنشاء مجموعة الاتصالات - Create connection pool
	pool, err := pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		return nil, fmt.Errorf("failed to create connection pool: %w", err)
	}

	// اختبار الاتصال - Test connection
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	return pool, nil
}

// DatabaseStats returns database connection pool statistics
// إحصائيات مجموعة اتصالات قاعدة البيانات
func (app *App) DatabaseStats() map[string]interface{} {
	stats := app.DB.Stat()
	return map[string]interface{}{
		"max_connections":      stats.MaxConns(),
		"acquired_connections": stats.AcquiredConns(),
		"idle_connections":     stats.IdleConns(),
		"total_connections":    stats.TotalConns(),
	}
}
