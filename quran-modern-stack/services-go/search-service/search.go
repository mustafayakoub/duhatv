// ═══════════════════════════════════════════════════════════════════════════
// Quran Search Logic
// منطق البحث في القرآن الكريم
//
// Features:
//   - Full-text search using PostgreSQL's built-in tsvector
//   - Arabic text normalization (removing diacritics, etc.)
//   - Trigram-based similarity search for finding similar verses
//   - Support for filtering by surah, juz, page
//   - Ranked results by relevance
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"context"
	"fmt"
	"regexp"
	"strings"
	"unicode"

	"github.com/jackc/pgx/v5"
)

// ═══════════════════════════════════════════════════════════════════════════
// Data Models (نماذج البيانات)
// ═══════════════════════════════════════════════════════════════════════════

// SearchParams contains search query parameters
// معاملات استعلام البحث
type SearchParams struct {
	Query    string // النص المراد البحث عنه
	Surah    int    // رقم السورة (اختياري)
	Juz      int    // رقم الجزء (اختياري)
	Page     int    // رقم الصفحة (اختياري)
	Language string // اللغة (ar, en)
	Limit    int    // الحد الأقصى للنتائج
	Offset   int    // الإزاحة للترقيم
}

// SearchResult represents a single search result
// نتيجة بحث واحدة
type SearchResult struct {
	AyahID              int     `json:"ayah_id"`
	SurahNumber         int     `json:"surah_number"`
	AyahNumber          int     `json:"ayah_number"`
	SurahNameArabic     string  `json:"surah_name_arabic"`
	SurahNameEn         string  `json:"surah_name_en"`
	TextUthmani         string  `json:"text_uthmani"`
	TextSimple          string  `json:"text_simple"`
	JuzNumber           *int    `json:"juz_number,omitempty"`
	PageNumber          *int    `json:"page_number,omitempty"`
	Translation         *string `json:"translation,omitempty"`
	Rank                float64 `json:"rank"`
	MatchedText         string  `json:"matched_text,omitempty"`
}

// SearchResponse contains search results and metadata
// استجابة البحث مع البيانات الوصفية
type SearchResponse struct {
	Results    []SearchResult `json:"results"`
	Total      int            `json:"total"`
	Query      string         `json:"query"`
	Limit      int            `json:"limit"`
	Offset     int            `json:"offset"`
	ExecutionTimeMS float64   `json:"execution_time_ms"`
}

// SimilarParams contains similarity search parameters
type SimilarParams struct {
	Text      string  // النص المراد البحث عن مشابهات له
	Threshold float64 // حد التشابه (0-1)
	Limit     int     // الحد الأقصى للنتائج
}

// ═══════════════════════════════════════════════════════════════════════════
// Arabic Text Normalization (تطبيع النص العربي)
// ═══════════════════════════════════════════════════════════════════════════

// NormalizeArabicText removes diacritics and normalizes Arabic text for search
// إزالة التشكيل وتطبيع النص العربي للبحث
func NormalizeArabicText(text string) string {
	// إزالة التشكيل - Remove Arabic diacritics
	text = removeDiacritics(text)

	// تطبيع الأحرف المتشابهة - Normalize similar letters
	replacements := map[rune]rune{
		'أ': 'ا',
		'إ': 'ا',
		'آ': 'ا',
		'ٱ': 'ا',
		'ة': 'ه',
		'ى': 'ي',
	}

	var normalized strings.Builder
	for _, r := range text {
		if replacement, ok := replacements[r]; ok {
			normalized.WriteRune(replacement)
		} else {
			normalized.WriteRune(r)
		}
	}

	// إزالة المسافات الزائدة - Remove extra whitespace
	text = strings.TrimSpace(normalized.String())
	text = regexp.MustCompile(`\s+`).ReplaceAllString(text, " ")

	return text
}

// removeDiacritics removes Arabic diacritical marks
// إزالة علامات التشكيل العربية
func removeDiacritics(text string) string {
	var result strings.Builder

	for _, r := range text {
		// Arabic diacritics range: U+064B to U+065F
		if r < 0x064B || r > 0x065F {
			// Also exclude tatweel (U+0640)
			if r != 0x0640 {
				result.WriteRune(r)
			}
		}
	}

	return result.String()
}

// containsArabic checks if text contains Arabic characters
// التحقق من وجود أحرف عربية في النص
func containsArabic(text string) bool {
	for _, r := range text {
		if unicode.In(r, unicode.Arabic) {
			return true
		}
	}
	return false
}

// ═══════════════════════════════════════════════════════════════════════════
// Search Implementation (تنفيذ البحث)
// ═══════════════════════════════════════════════════════════════════════════

// Search performs full-text search on Quran verses
// البحث النصي الكامل في آيات القرآن
func (app *App) Search(ctx context.Context, params SearchParams) ([]SearchResult, int, error) {
	// Normalize search query for Arabic text
	normalizedQuery := params.Query
	if containsArabic(params.Query) {
		normalizedQuery = NormalizeArabicText(params.Query)
	}

	// بناء استعلام SQL - Build SQL query
	query := `
		SELECT
			a.id,
			a.ayah_number,
			a.text_uthmani,
			a.text_simple,
			a.juz_number,
			a.page_number,
			s.number as surah_number,
			s.name_arabic as surah_name_arabic,
			s.name_transliteration as surah_name_en,
			ts_rank(a.search_vector, plainto_tsquery('arabic', $1)) as rank
		FROM ayahs a
		JOIN surahs s ON s.id = a.surah_id
		WHERE
			(
				a.search_vector @@ plainto_tsquery('arabic', $1)
				OR a.text_simple ILIKE '%' || $1 || '%'
			)
	`

	args := []interface{}{normalizedQuery}
	argIndex := 2

	// إضافة فلاتر - Add filters
	if params.Surah > 0 {
		query += fmt.Sprintf(" AND s.number = $%d", argIndex)
		args = append(args, params.Surah)
		argIndex++
	}

	if params.Juz > 0 {
		query += fmt.Sprintf(" AND a.juz_number = $%d", argIndex)
		args = append(args, params.Juz)
		argIndex++
	}

	if params.Page > 0 {
		query += fmt.Sprintf(" AND a.page_number = $%d", argIndex)
		args = append(args, params.Page)
		argIndex++
	}

	// ترتيب حسب الصلة - Order by relevance
	query += " ORDER BY rank DESC, a.id ASC"

	// الترقيم - Pagination
	if params.Limit > 0 {
		query += fmt.Sprintf(" LIMIT $%d", argIndex)
		args = append(args, params.Limit)
		argIndex++
	}

	if params.Offset > 0 {
		query += fmt.Sprintf(" OFFSET $%d", argIndex)
		args = append(args, params.Offset)
	}

	// تنفيذ الاستعلام - Execute query
	rows, err := app.DB.Query(ctx, query, args...)
	if err != nil {
		return nil, 0, fmt.Errorf("search query failed: %w", err)
	}
	defer rows.Close()

	// تحليل النتائج - Parse results
	var results []SearchResult
	for rows.Next() {
		var result SearchResult
		err := rows.Scan(
			&result.AyahID,
			&result.AyahNumber,
			&result.TextUthmani,
			&result.TextSimple,
			&result.JuzNumber,
			&result.PageNumber,
			&result.SurahNumber,
			&result.SurahNameArabic,
			&result.SurahNameEn,
			&result.Rank,
		)
		if err != nil {
			return nil, 0, fmt.Errorf("failed to scan result: %w", err)
		}

		// تمييز النص المطابق - Highlight matched text
		result.MatchedText = highlightMatch(result.TextSimple, normalizedQuery)

		results = append(results, result)
	}

	// احسب العدد الإجمالي - Get total count
	total := len(results)
	if params.Limit > 0 && len(results) == params.Limit {
		// Run count query if we hit the limit
		countQuery := `
			SELECT COUNT(*)
			FROM ayahs a
			JOIN surahs s ON s.id = a.surah_id
			WHERE
				(
					a.search_vector @@ plainto_tsquery('arabic', $1)
					OR a.text_simple ILIKE '%' || $1 || '%'
				)
		`
		countArgs := []interface{}{normalizedQuery}
		countArgIndex := 2

		if params.Surah > 0 {
			countQuery += fmt.Sprintf(" AND s.number = $%d", countArgIndex)
			countArgs = append(countArgs, params.Surah)
			countArgIndex++
		}

		if params.Juz > 0 {
			countQuery += fmt.Sprintf(" AND a.juz_number = $%d", countArgIndex)
			countArgs = append(countArgs, params.Juz)
			countArgIndex++
		}

		if params.Page > 0 {
			countQuery += fmt.Sprintf(" AND a.page_number = $%d", countArgIndex)
			countArgs = append(countArgs, params.Page)
		}

		err = app.DB.QueryRow(ctx, countQuery, countArgs...).Scan(&total)
		if err != nil {
			return results, len(results), nil // Return what we have
		}
	}

	return results, total, nil
}

// ═══════════════════════════════════════════════════════════════════════════
// Similar Search (البحث عن المتشابهات)
// ═══════════════════════════════════════════════════════════════════════════

// FindSimilar finds similar verses using trigram similarity
// البحث عن آيات مشابهة باستخدام trigram
func (app *App) FindSimilar(ctx context.Context, params SimilarParams) ([]SearchResult, error) {
	// تطبيع النص - Normalize text
	normalizedText := NormalizeArabicText(params.Text)

	query := `
		SELECT
			a.id,
			a.ayah_number,
			a.text_uthmani,
			a.text_simple,
			a.juz_number,
			a.page_number,
			s.number as surah_number,
			s.name_arabic as surah_name_arabic,
			s.name_transliteration as surah_name_en,
			similarity(a.text_simple, $1) as rank
		FROM ayahs a
		JOIN surahs s ON s.id = a.surah_id
		WHERE similarity(a.text_simple, $1) > $2
		ORDER BY rank DESC
		LIMIT $3
	`

	rows, err := app.DB.Query(ctx, query, normalizedText, params.Threshold, params.Limit)
	if err != nil {
		return nil, fmt.Errorf("similar search failed: %w", err)
	}
	defer rows.Close()

	var results []SearchResult
	for rows.Next() {
		var result SearchResult
		err := rows.Scan(
			&result.AyahID,
			&result.AyahNumber,
			&result.TextUthmani,
			&result.TextSimple,
			&result.JuzNumber,
			&result.PageNumber,
			&result.SurahNumber,
			&result.SurahNameArabic,
			&result.SurahNameEn,
			&result.Rank,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan similar result: %w", err)
		}

		results = append(results, result)
	}

	return results, nil
}

// ═══════════════════════════════════════════════════════════════════════════
// Auto-complete Suggestions (الاقتراحات التلقائية)
// ═══════════════════════════════════════════════════════════════════════════

// Suggestion represents an auto-complete suggestion
type Suggestion struct {
	Text  string  `json:"text"`
	Type  string  `json:"type"` // 'surah', 'ayah', 'word'
	Score float64 `json:"score"`
}

// GetSuggestions returns auto-complete suggestions
// الحصول على اقتراحات الإكمال التلقائي
func (app *App) GetSuggestions(ctx context.Context, query string, limit int) ([]Suggestion, error) {
	normalizedQuery := NormalizeArabicText(query)

	// البحث في أسماء السور - Search surah names
	surahQuery := `
		SELECT
			name_arabic,
			'surah' as type,
			similarity(name_arabic, $1) as score
		FROM surahs
		WHERE similarity(name_arabic, $1) > 0.3
		ORDER BY score DESC
		LIMIT $2
	`

	rows, err := app.DB.Query(ctx, surahQuery, normalizedQuery, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var suggestions []Suggestion
	for rows.Next() {
		var s Suggestion
		if err := rows.Scan(&s.Text, &s.Type, &s.Score); err != nil {
			continue
		}
		suggestions = append(suggestions, s)
	}

	return suggestions, nil
}

// ═══════════════════════════════════════════════════════════════════════════
// Helper Functions (دوال مساعدة)
// ═══════════════════════════════════════════════════════════════════════════

// highlightMatch highlights the matched text in the result
// تمييز النص المطابق في النتيجة
func highlightMatch(text, query string) string {
	if query == "" {
		return text
	}

	// Simple highlight - wrap matched text with markers
	normalizedText := NormalizeArabicText(text)
	normalizedQuery := NormalizeArabicText(query)

	if strings.Contains(normalizedText, normalizedQuery) {
		// Find position in original text
		words := strings.Fields(query)
		for _, word := range words {
			if len(word) > 2 {
				pattern := regexp.MustCompile(`(?i)` + regexp.QuoteMeta(word))
				text = pattern.ReplaceAllString(text, "<mark>$0</mark>")
			}
		}
	}

	return text
}

// GetAyahByID retrieves a single ayah by ID
// الحصول على آية بواسطة المعرف
func (app *App) GetAyahByID(ctx context.Context, ayahID int) (*SearchResult, error) {
	query := `
		SELECT
			a.id,
			a.ayah_number,
			a.text_uthmani,
			a.text_simple,
			a.juz_number,
			a.page_number,
			s.number as surah_number,
			s.name_arabic as surah_name_arabic,
			s.name_transliteration as surah_name_en
		FROM ayahs a
		JOIN surahs s ON s.id = a.surah_id
		WHERE a.id = $1
	`

	var result SearchResult
	err := app.DB.QueryRow(ctx, query, ayahID).Scan(
		&result.AyahID,
		&result.AyahNumber,
		&result.TextUthmani,
		&result.TextSimple,
		&result.JuzNumber,
		&result.PageNumber,
		&result.SurahNumber,
		&result.SurahNameArabic,
		&result.SurahNameEn,
	)

	if err == pgx.ErrNoRows {
		return nil, fmt.Errorf("ayah not found")
	}
	if err != nil {
		return nil, err
	}

	return &result, nil
}
