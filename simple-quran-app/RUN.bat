@echo off
chcp 65001 >nul
cls

echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo   🌙 تطبيق القرآن الكريم - تشغيل تلقائي
echo   Quran Simple Web App - Auto Launcher
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM التحقق من Python
echo [1/4] 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت!
    echo.
    echo 📥 حمّل Python من: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python مثبت
echo.

REM التحقق من المكتبات
echo [2/4] 📦 التحقق من المكتبات المطلوبة...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask غير مثبت - جارٍ التثبيت...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ فشل تثبيت المكتبات
        pause
        exit /b 1
    )
) else (
    echo ✅ كل المكتبات مثبتة
)
echo.

REM التحقق من قواعد البيانات
echo [3/4] 📊 التحقق من قواعد البيانات...
set DB_FOUND=0
if exist "C:\quran11\quran_ultimate_final.db" (
    echo ✅ DB1 موجود
    set DB_FOUND=1
)
if exist "C:\quran11\surah_database_app_v32.db" (
    echo ✅ DB2 موجود
    set DB_FOUND=1
)
if exist "C:\quran11\Quran_Crystalline.db" (
    echo ✅ DB3 موجود
    set DB_FOUND=1
)

if %DB_FOUND%==0 (
    echo.
    echo ⚠️  تحذير: لم يتم العثور على قواعد البيانات في C:\quran11\
    echo.
    echo 📁 ضع ملفات قواعد البيانات في:
    echo    C:\quran11\quran_ultimate_final.db
    echo    C:\quran11\surah_database_app_v32.db
    echo    C:\quran11\Quran_Crystalline.db
    echo.
    echo التطبيق سيعمل لكن بدون بيانات!
    echo.
    timeout /t 5
)
echo.

REM تشغيل التطبيق
echo [4/4] 🚀 تشغيل التطبيق...
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo   🌐 التطبيق سيفتح على: http://localhost:5000
echo ═══════════════════════════════════════════════════════════════════════════
echo.
timeout /t 3 /nobreak >nul

REM فتح المتصفح
start http://localhost:5000

REM تشغيل Flask
python app.py

pause
