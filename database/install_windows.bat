@echo off
REM ═══════════════════════════════════════════════════════════════
REM 🚀 سكريبت تنفيذ قاعدة البيانات القرآنية على Windows
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo 📖 تنفيذ قاعدة البيانات القرآنية الهرمية
echo ═══════════════════════════════════════════════════════════════
echo.

REM التحقق من وجود PostgreSQL
where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PostgreSQL غير مثبت أو غير موجود في PATH
    echo.
    echo يرجى تثبيت PostgreSQL من:
    echo https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo ✅ تم العثور على PostgreSQL
psql --version
echo.

REM إعدادات الاتصال (عدّلها حسب إعداداتك)
set PGHOST=localhost
set PGPORT=5432
set PGUSER=postgres
set PGPASSWORD=

echo.
echo 📝 إعدادات الاتصال:
echo    Host: %PGHOST%
echo    Port: %PGPORT%
echo    User: %PGUSER%
echo.

REM اسأل عن كلمة المرور
set /p PGPASSWORD="🔐 أدخل كلمة مرور PostgreSQL: "

REM التحقق من الاتصال
echo.
echo 🔍 التحقق من الاتصال...
psql -U %PGUSER% -c "SELECT version();" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ فشل الاتصال بـ PostgreSQL
    echo تأكد من:
    echo   - خدمة PostgreSQL تعمل
    echo   - كلمة المرور صحيحة
    echo   - المنفذ 5432 مفتوح
    pause
    exit /b 1
)

echo ✅ نجح الاتصال!
echo.

REM البحث عن ملفات SQL
set SCRIPT_DIR=%~dp0database\sql

if not exist "%SCRIPT_DIR%" (
    echo ❌ مجلد SQL غير موجود: %SCRIPT_DIR%
    echo.
    echo يرجى التأكد من وجود المجلد database\sql
    pause
    exit /b 1
)

echo 📂 مجلد السكريبتات: %SCRIPT_DIR%
echo.

REM تنفيذ السكريبتات بالترتيب
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔨 المرحلة 1: الإعداد الأولي
echo ═══════════════════════════════════════════════════════════════
echo.

psql -U %PGUSER% -f "%SCRIPT_DIR%\01_setup.sql"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ فشل تنفيذ 01_setup.sql
    pause
    exit /b 1
)

echo.
echo ✅ تم إنشاء القاعدة والامتدادات بنجاح!
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔨 المرحلة 2: الجداول الأساسية (النواة)
echo ═══════════════════════════════════════════════════════════════
echo.

psql -U %PGUSER% -d quran_hierarchical_db -f "%SCRIPT_DIR%\02_level0_core_tables.sql"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ فشل تنفيذ 02_level0_core_tables.sql
    pause
    exit /b 1
)

echo.
echo ✅ تم إنشاء الجداول الأساسية بنجاح!
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔨 المرحلة 3: الجداول المتبقية
echo ═══════════════════════════════════════════════════════════════
echo.

psql -U %PGUSER% -d quran_hierarchical_db -f "%SCRIPT_DIR%\03_remaining_levels.sql"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ فشل تنفيذ 03_remaining_levels.sql
    pause
    exit /b 1
)

echo.
echo ✅ تم إنشاء جميع الجداول بنجاح!
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🔨 المرحلة 4: Views والدوال
echo ═══════════════════════════════════════════════════════════════
echo.

psql -U %PGUSER% -d quran_hierarchical_db -f "%SCRIPT_DIR%\04_views_and_functions.sql"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ فشل تنفيذ 04_views_and_functions.sql
    pause
    exit /b 1
)

echo.
echo ✅ تم إنشاء Views والدوال بنجاح!
echo.

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎉 تم التنفيذ بنجاح!
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📊 تفاصيل القاعدة:
echo    الاسم: quran_hierarchical_db
echo    الجداول: 19 جدول
echo    الأعمدة: 400+ عمود
echo.
echo 🔍 للاتصال:
echo    psql -U %PGUSER% -d quran_hierarchical_db
echo.
echo 📚 للمزيد من المعلومات:
echo    - database\README.md
echo    - database\SMART_QUERIES.md
echo.

pause
