// ═══════════════════════════════════════════════════════════════════════════
// Quran Search Service - Tests
// اختبارات خدمة البحث
// ═══════════════════════════════════════════════════════════════════════════

package main

import (
	"testing"
)

// ═══════════════════════════════════════════════════════════════════════════
// Arabic Text Normalization Tests
// اختبارات تطبيع النص العربي
// ═══════════════════════════════════════════════════════════════════════════

func TestNormalizeArabicText(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Remove diacritics",
			input:    "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
			expected: "بسم الله الرحمن الرحيم",
		},
		{
			name:     "Normalize alif variants",
			input:    "أإآٱ",
			expected: "اااا",
		},
		{
			name:     "Normalize ta marbuta",
			input:    "الفاتحة",
			expected: "الفاتحه",
		},
		{
			name:     "Normalize alif maqsura",
			input:    "موسى",
			expected: "موسي",
		},
		{
			name:     "Remove tatweel",
			input:    "اللـــــه",
			expected: "الله",
		},
		{
			name:     "Multiple spaces",
			input:    "بسم  الله   الرحمن",
			expected: "بسم الله الرحمن",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := NormalizeArabicText(tt.input)
			if result != tt.expected {
				t.Errorf("NormalizeArabicText(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestRemoveDiacritics(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Fatha",
			input:    "بَ",
			expected: "ب",
		},
		{
			name:     "Damma",
			input:    "بُ",
			expected: "ب",
		},
		{
			name:     "Kasra",
			input:    "بِ",
			expected: "ب",
		},
		{
			name:     "Sukun",
			input:    "بْ",
			expected: "ب",
		},
		{
			name:     "Shadda",
			input:    "بّ",
			expected: "ب",
		},
		{
			name:     "Tanween Fath",
			input:    "بً",
			expected: "ب",
		},
		{
			name:     "Mixed diacritics",
			input:    "بِسْمِ ٱللَّهِ",
			expected: "بسم الله",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := removeDiacritics(tt.input)
			if result != tt.expected {
				t.Errorf("removeDiacritics(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestContainsArabic(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{
			name:     "Pure Arabic",
			input:    "بسم الله",
			expected: true,
		},
		{
			name:     "Arabic with diacritics",
			input:    "بِسْمِ ٱللَّهِ",
			expected: true,
		},
		{
			name:     "Mixed Arabic and English",
			input:    "Quran القرآن",
			expected: true,
		},
		{
			name:     "Pure English",
			input:    "Hello World",
			expected: false,
		},
		{
			name:     "Numbers only",
			input:    "12345",
			expected: false,
		},
		{
			name:     "Empty string",
			input:    "",
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := containsArabic(tt.input)
			if result != tt.expected {
				t.Errorf("containsArabic(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		})
	}
}

// ═══════════════════════════════════════════════════════════════════════════
// Cache Key Generation Tests
// اختبارات إنشاء مفاتيح الكاش
// ═══════════════════════════════════════════════════════════════════════════

func TestGenerateCacheKey(t *testing.T) {
	tests := []struct {
		name     string
		prefix   string
		params   []string
		expected string // We check for consistency, not exact value
	}{
		{
			name:   "Simple key",
			prefix: "search:",
			params: []string{"الله"},
		},
		{
			name:   "Multiple parameters",
			prefix: "search:",
			params: []string{"الله", "1", "ar"},
		},
		{
			name:   "Empty parameters",
			prefix: "suggest:",
			params: []string{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			key1 := GenerateCacheKey(tt.prefix, tt.params...)
			key2 := GenerateCacheKey(tt.prefix, tt.params...)

			// Keys should be consistent
			if key1 != key2 {
				t.Errorf("GenerateCacheKey is not consistent: %q != %q", key1, key2)
			}

			// Key should start with prefix
			if len(key1) < len(tt.prefix) || key1[:len(tt.prefix)] != tt.prefix {
				t.Errorf("GenerateCacheKey doesn't start with prefix: %q", key1)
			}
		})
	}
}

// ═══════════════════════════════════════════════════════════════════════════
// Benchmark Tests
// اختبارات الأداء
// ═══════════════════════════════════════════════════════════════════════════

func BenchmarkNormalizeArabicText(b *testing.B) {
	text := "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ ۝ ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		NormalizeArabicText(text)
	}
}

func BenchmarkRemoveDiacritics(b *testing.B) {
	text := "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		removeDiacritics(text)
	}
}

func BenchmarkGenerateCacheKey(b *testing.B) {
	params := []string{"الله", "1", "ar", "20", "0"}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		GenerateCacheKey("search:", params...)
	}
}

// ═══════════════════════════════════════════════════════════════════════════
// Example Tests (Documentation)
// أمثلة الاختبارات (للتوثيق)
// ═══════════════════════════════════════════════════════════════════════════

func ExampleNormalizeArabicText() {
	text := "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
	normalized := NormalizeArabicText(text)
	println(normalized)
	// Output is deterministic
}

func ExampleGenerateCacheKey() {
	key := GenerateCacheKey("search:", "الله", "1")
	println(key)
	// Output starts with "search:"
}
