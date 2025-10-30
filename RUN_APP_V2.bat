@echo off
chcp 65001 > nul
title تشغيل تطبيق القرآن الكريم الاحترافي v2.1 Final

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          تطبيق القرآن الكريم الاحترافي 2.1 Final               ║
echo ║          Professional Quran Application                          ║
echo ║                                                                  ║
echo ║          ✨ النسخة المحدثة والذكية ✨                            ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.

:: التحقق من وجود Python
echo [1/4] التحقق من Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo.
    echo الرجاء تثبيت Python من:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python مثبت

:: التحقق من PyQt
echo.
echo [2/4] التحقق من المكتبات...
python -c "import PyQt6" > nul 2>&1
if errorlevel 1 (
    python -c "import PyQt5" > nul 2>&1
    if errorlevel 1 (
        echo ⚠️  PyQt غير مثبت
        echo.
        echo هل تريد تثبيت PyQt6 الآن؟ [Y/N]
        set /p install_pyqt=
        if /i "%install_pyqt%"=="Y" (
            echo.
            echo جاري التثبيت...
            pip install PyQt6
            if errorlevel 1 (
                echo ❌ فشل التثبيت
                pause
                exit /b 1
            )
            echo ✅ تم التثبيت بنجاح
        ) else (
            echo ❌ لا يمكن تشغيل التطبيق بدون PyQt
            pause
            exit /b 1
        )
    ) else (
        echo ✅ PyQt5 مثبت
    )
) else (
    echo ✅ PyQt6 مثبت
)

:: التحقق من قاعدة البيانات
echo.
echo [3/4] التحقق من قاعدة البيانات...
set DB_FOUND=0

if exist "C:\QYRAN5\QYRAN62\*.db" (
    echo ✅ تم العثور على قاعدة البيانات في C:\QYRAN5\QYRAN62\
    set DB_FOUND=1
)

if exist "*.db" (
    echo ✅ تم العثور على قاعدة البيانات في المجلد الحالي
    set DB_FOUND=1
)

if %DB_FOUND%==0 (
    echo ⚠️  تحذير: لم يتم العثور على قاعدة البيانات
    echo.
    echo الرجاء وضع ملف قاعدة البيانات في:
    echo   C:\QYRAN5\QYRAN62\
    echo   أو في نفس المجلد مع التطبيق
    echo.
    echo هل تريد المتابعة على أي حال؟ [Y/N]
    set /p continue_anyway=
    if /i not "%continue_anyway%"=="Y" (
        pause
        exit /b 1
    )
)

:: تشغيل التطبيق
echo.
echo [4/4] تشغيل التطبيق النهائي...
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
echo ✨ النسخة 2.1 Final - محدثة وذكية ✨
echo.
echo الميزات الجديدة:
echo   • دعم ذكي لأسماء الأعمدة المختلفة
echo   • تفاسير متعددة (الميسر، السعدي، البغوي)
echo   • تنقل محسّن (السابق/التالي)
echo   • بحث أسرع وأذكى
echo   • واجهة أكثر احترافية
echo.
echo ══════════════════════════════════════════════════════════════════
echo.

python quran_app_v2_final.py

echo.
echo ══════════════════════════════════════════════════════════════════
echo.

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ أثناء تشغيل التطبيق
    echo.
    echo جرب النسخة الأولى: RUN_APP.bat
    echo.
) else (
    echo.
    echo ✅ تم إغلاق التطبيق بنجاح
    echo.
)

pause
