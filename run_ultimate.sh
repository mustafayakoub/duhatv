#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 🚀 تشغيل القرآن الكريم Ultimate v3.0
# ═══════════════════════════════════════════════════════════════

cd "$(dirname "$0")"

echo "═══════════════════════════════════════════════════════════════"
echo "📖 القرآن الكريم Ultimate v3.0"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    exit 1
fi

# التحقق من المتطلبات
echo "🔍 التحقق من المتطلبات..."

if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  PyQt6 غير مثبت - جاري التثبيت..."
    pip3 install PyQt6
fi

# التحقق من psycopg2 (اختياري)
if ! python3 -c "import psycopg2" 2>/dev/null; then
    echo "⚠️  psycopg2 غير مثبت (PostgreSQL)"
    echo "   للتثبيت: pip3 install psycopg2-binary"
    echo "   سيعمل التطبيق مع SQLite فقط"
    echo ""
fi

# تشغيل التطبيق
echo "🚀 تشغيل التطبيق..."
echo ""

python3 quran_ultimate.py

echo ""
echo "✅ تم إغلاق التطبيق"
