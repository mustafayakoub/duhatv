@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM Quran Modern Stack - Windows Startup Script
REM نص تشغيل تلقائي لـ Windows
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo   🚀 Quran Modern Stack - نظام قرآني متكامل
echo   ⚡ Ultra-Fast Multilingual System
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM التحقق من Docker
echo [1/5] 🔍 التحقق من Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Docker غير مثبت!
    echo 📥 حمّل Docker Desktop من: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✅ Docker مثبت

REM التحقق من تشغيل Docker
echo.
echo [2/5] 🐳 التحقق من تشغيل Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Docker غير مُشغّل!
    echo 💡 افتح Docker Desktop وانتظر حتى يبدأ
    pause
    exit /b 1
)
echo ✅ Docker يعمل

REM إيقاف الخدمات القديمة (إن وجدت)
echo.
echo [3/5] 🛑 إيقاف الخدمات القديمة (إن وجدت)...
docker-compose down 2>nul

REM تشغيل الخدمات
echo.
echo [4/5] 🚀 تشغيل الخدمات...
echo.
docker-compose up -d

if errorlevel 1 (
    echo ❌ خطأ في تشغيل الخدمات!
    echo 📋 راجع اللوجز: docker-compose logs
    pause
    exit /b 1
)

REM انتظار بدء الخدمات
echo.
echo [5/5] ⏳ انتظار بدء الخدمات...
timeout /t 5 /nobreak >nul

REM عرض الحالة
echo.
echo ═══════════════════════════════════════════════════════════════════════════
docker-compose ps
echo ═══════════════════════════════════════════════════════════════════════════

REM اختبار الخدمات
echo.
echo 🧪 اختبار الخدمات...
echo.

echo 1. PostgreSQL:
docker-compose exec -T postgres pg_isready -U quran
if errorlevel 1 (
    echo ⚠️  PostgreSQL لم يبدأ بعد - انتظر قليلاً
) else (
    echo ✅ PostgreSQL جاهز
)

echo.
echo 2. Rust API:
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Rust API لم يبدأ بعد - انتظر قليلاً
) else (
    echo ✅ Rust API جاهز
)

REM عرض الروابط
echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo   🌐 الروابط:
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo   🦀 Rust API:        http://localhost:8000
echo   🦀 Health Check:    http://localhost:8000/health
echo   🦀 Surahs:          http://localhost:8000/api/v1/surahs
echo.
echo ═══════════════════════════════════════════════════════════════════════════

echo.
echo ✅ النظام يعمل الآن!
echo.
echo 📋 أوامر مفيدة:
echo    - عرض اللوجز:     docker-compose logs -f
echo    - إيقاف الخدمات:  docker-compose down
echo    - إعادة التشغيل:  docker-compose restart
echo.

REM فتح المتصفح
echo 🌐 فتح المتصفح...
timeout /t 2 /nobreak >nul
start http://localhost:8000/health

echo.
pause
