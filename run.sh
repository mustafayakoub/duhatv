#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# تشغيل تطبيق القرآن الكريم Pro - Linux/Mac
# ═══════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "📖 تشغيل تطبيق القرآن الكريم Pro"
echo "═══════════════════════════════════════════════════════════════"

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    echo "الرجاء تثبيت Python 3.8 أو أحدث"
    exit 1
fi

echo "✅ Python 3 موجود"

# التحقق من قاعدة البيانات
if [ ! -f "data/quran_ultimate_final.db" ]; then
    echo "❌ قاعدة البيانات غير موجودة في data/"
    echo "الرجاء وضع ملف quran_ultimate_final.db في مجلد data/"
    exit 1
fi

echo "✅ قاعدة البيانات موجودة"

# التحقق من PyQt6
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  PyQt6 غير مثبت"
    echo "جارٍ التثبيت..."
    pip3 install -r requirements.txt
fi

echo "✅ PyQt6 جاهز"
echo ""
echo "🚀 بدء التطبيق..."
echo ""

# تشغيل التطبيق
python3 quran_pro.py

echo ""
echo "═══════════════════════════════════════════════════════════════"
