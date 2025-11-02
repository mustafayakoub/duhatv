// ═══════════════════════════════════════════════════════════════════════════
// Quran Modern Stack - Go Search Microservice
// خدمة البحث السريع في القرآن الكريم - مكتوبة بـ Go
//
// Features:
//   - Fast Arabic text search using PostgreSQL Full-Text Search
//   - Redis caching for improved performance
//   - Similar verse search using trigram matching
//   - Production-ready with proper error handling and logging
//
// Author: Quran Modern Stack Team
// Version: 1.0.0
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/redis/go-redis/v9"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

// ═══════════════════════════════════════════════════════════════════════════
// Application State (حالة التطبيق)
// ═══════════════════════════════════════════════════════════════════════════

type App struct {
	DB     *pgxpool.Pool
	Cache  *redis.Client
	Router *chi.Mux
	Config *Config
}

type Config struct {
	Port        string
	DatabaseURL string
	RedisURL    string
	Environment string
	LogLevel    string
}

// ═══════════════════════════════════════════════════════════════════════════
// Main Entry Point (نقطة الدخول الرئيسية)
// ═══════════════════════════════════════════════════════════════════════════

func main() {
	// إعداد السجلات - Setup logging
	setupLogging()

	log.Info().Msg("🚀 Starting Quran Search Service...")

	// تحميل الإعدادات - Load configuration
	config := loadConfig()
	log.Info().
		Str("environment", config.Environment).
		Str("port", config.Port).
		Msg("Configuration loaded")

	// إنشاء التطبيق - Create application
	app, err := NewApp(config)
	if err != nil {
		log.Fatal().Err(err).Msg("Failed to create application")
	}
	defer app.Close()

	// إعداد المسارات - Setup routes
	app.setupRoutes()

	// بدء الخادم - Start server
	server := &http.Server{
		Addr:         ":" + config.Port,
		Handler:      app.Router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// قناة للإشارات - Channel for signals
	done := make(chan bool, 1)
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	// بدء الخادم في goroutine منفصل - Start server in separate goroutine
	go func() {
		log.Info().Str("address", server.Addr).Msg("🎯 Server is listening")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal().Err(err).Msg("Server failed to start")
		}
	}()

	// انتظار إشارة الإيقاف - Wait for shutdown signal
	<-quit
	log.Info().Msg("⏹️  Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatal().Err(err).Msg("Server forced to shutdown")
	}

	close(done)
	log.Info().Msg("✅ Server stopped gracefully")
}

// ═══════════════════════════════════════════════════════════════════════════
// Application Setup (إعداد التطبيق)
// ═══════════════════════════════════════════════════════════════════════════

// NewApp creates a new application instance with database and cache connections
// إنشاء نسخة جديدة من التطبيق مع اتصالات قاعدة البيانات والكاش
func NewApp(config *Config) (*App, error) {
	ctx := context.Background()

	// الاتصال بقاعدة البيانات - Connect to database
	log.Info().Msg("📊 Connecting to PostgreSQL...")
	db, err := connectDB(ctx, config.DatabaseURL)
	if err != nil {
		return nil, fmt.Errorf("database connection failed: %w", err)
	}
	log.Info().Msg("✅ PostgreSQL connected")

	// الاتصال بـ Redis - Connect to Redis
	log.Info().Msg("🔴 Connecting to Redis...")
	cache, err := connectRedis(ctx, config.RedisURL)
	if err != nil {
		// Redis is optional, log warning but continue
		log.Warn().Err(err).Msg("Redis connection failed, continuing without cache")
		cache = nil
	} else {
		log.Info().Msg("✅ Redis connected")
	}

	return &App{
		DB:     db,
		Cache:  cache,
		Router: chi.NewRouter(),
		Config: config,
	}, nil
}

// Close closes all connections
// إغلاق جميع الاتصالات
func (app *App) Close() {
	if app.DB != nil {
		app.DB.Close()
		log.Info().Msg("Database connection closed")
	}
	if app.Cache != nil {
		app.Cache.Close()
		log.Info().Msg("Redis connection closed")
	}
}

// setupRoutes configures all HTTP routes
// إعداد جميع مسارات HTTP
func (app *App) setupRoutes() {
	r := app.Router

	// Middleware
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(LoggerMiddleware)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Compress(5))
	r.Use(middleware.Timeout(30 * time.Second))

	// CORS Configuration
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"http://localhost:3000", "http://localhost:8000"},
		AllowedMethods:   []string{"GET", "POST", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-Request-ID"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300,
	}))

	// Routes
	r.Get("/health", app.handleHealth)
	r.Get("/metrics", app.handleMetrics)

	// API Routes
	r.Route("/api", func(r chi.Router) {
		r.Get("/search", app.handleSearch)
		r.Get("/similar", app.handleSimilar)
		r.Get("/suggest", app.handleSuggest)
	})

	// 404 handler
	r.NotFound(func(w http.ResponseWriter, r *http.Request) {
		respondJSON(w, http.StatusNotFound, map[string]string{
			"error": "Route not found",
		})
	})
}

// ═══════════════════════════════════════════════════════════════════════════
// Configuration Loading (تحميل الإعدادات)
// ═══════════════════════════════════════════════════════════════════════════

func loadConfig() *Config {
	return &Config{
		Port:        getEnv("PORT", "8001"),
		DatabaseURL: getEnv("DATABASE_URL", "postgresql://quran:quran_secure_pass_2025@localhost:5432/quran_db"),
		RedisURL:    getEnv("REDIS_URL", "redis://:redis_secure_pass_2025@localhost:6379/0"),
		Environment: getEnv("GO_ENV", "development"),
		LogLevel:    getEnv("LOG_LEVEL", "info"),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// ═══════════════════════════════════════════════════════════════════════════
// Logging Setup (إعداد السجلات)
// ═══════════════════════════════════════════════════════════════════════════

func setupLogging() {
	// Pretty console logging for development
	log.Logger = log.Output(zerolog.ConsoleWriter{
		Out:        os.Stdout,
		TimeFormat: time.RFC3339,
	})

	// Set log level
	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	if os.Getenv("LOG_LEVEL") == "debug" {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	}

	// Add caller information
	log.Logger = log.With().Caller().Logger()
}

// LoggerMiddleware is a custom HTTP logging middleware
// Middleware مخصص لتسجيل طلبات HTTP
func LoggerMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		ww := middleware.NewWrapResponseWriter(w, r.ProtoMajor)
		next.ServeHTTP(ww, r)

		duration := time.Since(start)

		log.Info().
			Str("method", r.Method).
			Str("path", r.URL.Path).
			Int("status", ww.Status()).
			Dur("duration", duration).
			Str("remote_addr", r.RemoteAddr).
			Msg("HTTP request")
	})
}
