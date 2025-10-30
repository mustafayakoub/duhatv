@echo off
chcp 65001 > nul
title تطبيق القرآن الكريم v3.0 Ultimate
color 0A

echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo                    تطبيق القرآن الكريم v3.0 Ultimate Edition
echo                      Ultimate Professional Quran Application
echo ════════════════════════════════════════════════════════════════════════════════
echo.
echo    المطور: Claude AI Assistant
echo    التاريخ: 2025-10-30
echo    النسخة: 3.0 Ultimate - البناء الذكي المتكامل
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo.

REM فحص وجود Python
echo [1/5] فحص تثبيت Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ خطأ: Python غير مثبت على جهازك
    echo.
    echo 📥 يرجى تحميل وتثبيت Python من:
    echo    https://www.python.org/downloads/
    echo.
    echo 💡 تأكد من تفعيل خيار "Add Python to PATH" أثناء التثبيت
    echo.
    pause
    exit /b 1
)
echo ✅ Python مثبت

echo.
echo [2/5] فحص PyQt6...
python -c "import PyQt6" > nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyQt6 غير مثبت
    echo.
    echo [3/5] تثبيت PyQt6...
    pip install PyQt6
    if errorlevel 1 (
        echo ❌ فشل تثبيت PyQt6
        pause
        exit /b 1
    )
) else (
    echo ✅ PyQt6 مثبت
)

echo.
echo [4/5] فحص ملف قاعدة البيانات...
if exist "quran.db" (
    echo ✅ تم العثور على quran.db
) else if exist "quran.sqlite" (
    echo ✅ تم العثور على quran.sqlite
) else if exist "data\quran.db" (
    echo ✅ تم العثور على data\quran.db
) else (
    echo ⚠️  تحذير: لم يتم العثور على ملف قاعدة البيانات
    echo    سيتم تشغيل التطبيق لكن قد لا يعمل بشكل صحيح
    echo    ضع ملف quran.db في نفس مجلد التطبيق
)

echo.
echo [5/5] تشغيل التطبيق...
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo                           🚀 جاري التشغيل...
echo ════════════════════════════════════════════════════════════════════════════════
echo.

python quran_app_v3_ultimate.py

if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════════════════════════════════════════════
    echo ❌ حدث خطأ أثناء تشغيل التطبيق
    echo ════════════════════════════════════════════════════════════════════════════════
    echo.
    echo 💡 نصائح لحل المشكلة:
    echo    1. تأكد من تثبيت PyQt6: pip install PyQt6
    echo    2. تأكد من وجود ملف quran.db في نفس المجلد
    echo    3. تحقق من رسالة الخطأ أعلاه
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo                           ✅ تم إغلاق التطبيق بنجاح
echo ════════════════════════════════════════════════════════════════════════════════
echo.
pause
