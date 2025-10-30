@echo off
REM ═══════════════════════════════════════════════════════════════
REM تشغيل تطبيق القرآن الكريم Pro - Windows
REM ═══════════════════════════════════════════════════════════════

chcp 65001 > nul
echo ═══════════════════════════════════════════════════════════════
echo 📖 تشغيل تطبيق القرآن الكريم Pro
echo ═══════════════════════════════════════════════════════════════

REM التحقق من Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت
    echo الرجاء تثبيت Python 3.8 أو أحدث من python.org
    pause
    exit /b 1
)

echo ✅ Python موجود

REM التحقق من قاعدة البيانات
if not exist "data\quran_ultimate_final.db" (
    echo ❌ قاعدة البيانات غير موجودة في data\
    echo الرجاء وضع ملف quran_ultimate_final.db في مجلد data\
    pause
    exit /b 1
)

echo ✅ قاعدة البيانات موجودة

REM التحقق من PyQt6
python -c "import PyQt6" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  PyQt6 غير مثبت
    echo جارٍ التثبيت...
    pip install -r requirements.txt
)

echo ✅ PyQt6 جاهز
echo.
echo 🚀 بدء التطبيق...
echo.

REM تشغيل التطبيق
python quran_pro.py

echo.
echo ═══════════════════════════════════════════════════════════════
pause
