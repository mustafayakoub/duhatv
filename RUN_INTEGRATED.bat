@echo off
chcp 65001 > nul
title 🕌 تطبيق القرآن الكريم المتكامل v3.0
color 0A

echo ================================================================================
echo.
echo            🕌 تطبيق القرآن الكريم المتكامل v3.0
echo            Ultimate Integrated Quran Application
echo.
echo ================================================================================
echo.

REM التحقق من وجود Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت!
    echo.
    echo يرجى تثبيت Python من:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python مثبت
python --version
echo.

REM التحقق من وجود PyQt6 أو PyQt5
echo 🔍 فحص المكتبات المطلوبة...
python -c "import PyQt6" > nul 2>&1
if errorlevel 1 (
    python -c "import PyQt5" > nul 2>&1
    if errorlevel 1 (
        echo.
        echo ⚠️ تحذير: PyQt6 و PyQt5 غير مثبتين!
        echo.
        echo هل تريد تثبيت PyQt6 الآن؟ (y/n)
        set /p install_choice=

        if /i "%install_choice%"=="y" (
            echo.
            echo 📦 جاري تثبيت PyQt6...
            pip install PyQt6
            echo.
            if errorlevel 1 (
                echo ❌ فشل التثبيت!
                echo جرب يدوياً: pip install PyQt6
                pause
                exit /b 1
            )
            echo ✅ تم التثبيت بنجاح!
            echo.
        ) else (
            echo.
            echo ❌ لا يمكن تشغيل التطبيق بدون PyQt6 أو PyQt5
            echo.
            echo قم بتشغيل أحد الأوامر التالية:
            echo   pip install PyQt6
            echo   pip install PyQt5
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo ✅ PyQt5 مثبت
    )
) else (
    echo ✅ PyQt6 مثبت
)

echo.

REM التحقق من وجود قاعدة بيانات
echo 🔍 فحص قواعد البيانات...

set found_db=0

if exist "quran_ultimate_final.db" (
    echo ✅ quran_ultimate_final.db موجودة
    set found_db=1
)

if exist "surah_database_app_v32.db" (
    echo ✅ surah_database_app_v32.db موجودة
    set found_db=1
)

if exist "Quran_Crystalline.db" (
    echo ✅ Quran_Crystalline.db موجودة
    set found_db=1
)

if exist "C:\quran9\quran_ultimate_final.db" (
    echo ✅ C:\quran9\quran_ultimate_final.db موجودة
    set found_db=1
)

if exist "C:\quran9\surah_database_app_v32.db" (
    echo ✅ C:\quran9\surah_database_app_v32.db موجودة
    set found_db=1
)

if exist "C:\quran9\Quran_Crystalline.db" (
    echo ✅ C:\quran9\Quran_Crystalline.db موجودة
    set found_db=1
)

if %found_db%==0 (
    echo.
    echo ⚠️ تحذير: لم يتم العثور على أي قاعدة بيانات!
    echo.
    echo يرجى وضع أحد الملفات التالية في نفس المجلد:
    echo   • quran_ultimate_final.db
    echo   • surah_database_app_v32.db
    echo   • Quran_Crystalline.db
    echo.
    echo أو ضعها في: C:\quran9\
    echo.
    echo هل تريد المتابعة على أي حال؟ (y/n)
    set /p continue_choice=

    if /i not "%continue_choice%"=="y" (
        echo.
        echo 🛑 تم الإلغاء
        pause
        exit /b 1
    )
)

echo.
echo ================================================================================
echo                        🚀 تشغيل التطبيق...
echo ================================================================================
echo.

REM تشغيل التطبيق
python quran_app_ultimate_integrated.py

if errorlevel 1 (
    echo.
    echo ================================================================================
    echo.
    echo ❌ حدث خطأ أثناء تشغيل التطبيق!
    echo.
    echo الأخطاء الشائعة وحلولها:
    echo ────────────────────────────────────────────────────────────────────────────
    echo.
    echo 1. خطأ: No module named 'PyQt6'
    echo    الحل: pip install PyQt6
    echo.
    echo 2. خطأ: لم يتم العثور على قاعدة بيانات
    echo    الحل: ضع ملف .db في نفس المجلد
    echo.
    echo 3. خطأ: Python غير موجود
    echo    الحل: ثبّت Python من python.org
    echo.
    echo ────────────────────────────────────────────────────────────────────────────
    echo.
    echo للمزيد من المساعدة، راجع ملف: README_INTEGRATED.md
    echo.
    echo ================================================================================
) else (
    echo.
    echo ================================================================================
    echo.
    echo ✅ تم إغلاق التطبيق بنجاح
    echo.
    echo شكراً لاستخدامك تطبيق القرآن الكريم المتكامل ✨
    echo.
    echo ================================================================================
)

echo.
pause
