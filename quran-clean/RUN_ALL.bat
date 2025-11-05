@echo off
chcp 65001 > nul
echo.
echo ============================================
echo    تطبيق القرآن النظيف - Quran Clean
echo ============================================
echo.

REM التحقق من وجود الملفات
wsl bash -c "ls /home/user/duhatv/quran-clean/data/ayat/*.txt 2>/dev/null | head -1" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  لم يتم نسخ الملفات بعد!
    echo.
    echo الرجاء تشغيل الأمر التالي أولاً:
    echo   powershell -ExecutionPolicy Bypass -File "\\wsl$\Ubuntu\home\user\duhatv\quran-clean\COPY_FILES.ps1"
    echo.
    echo أو نسخ الملفات يدوياً من C:\Qgo3\ إلى:
    echo   \\wsl$\Ubuntu\home\user\duhatv\quran-clean\data\
    echo.
    pause
    exit /b 1
)

echo ✅ الملفات موجودة
echo.

REM التحقق من وجود قاعدة البيانات
wsl bash -c "test -f /home/user/duhatv/quran-clean/quran.db"
if %ERRORLEVEL% NEQ 0 (
    echo 📊 قاعدة البيانات غير موجودة، جارٍ الاستيراد...
    echo ⏱️  هذا قد يستغرق 5-10 دقائق
    echo.

    echo 1️⃣  تثبيت المتطلبات...
    wsl bash -c "cd /home/user/duhatv/quran-clean && pip install -r requirements.txt"

    echo.
    echo 2️⃣  استيراد البيانات...
    wsl bash -c "cd /home/user/duhatv/quran-clean && python import_data.py"

    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ فشل استيراد البيانات!
        pause
        exit /b 1
    )

    echo.
    echo ✅ تم استيراد البيانات بنجاح!
    echo.
) else (
    echo ✅ قاعدة البيانات موجودة
    echo.
)

echo 🚀 تشغيل التطبيق...
echo.
echo 🌐 افتح المتصفح على: http://localhost:5000
echo.
echo 🛑 لإيقاف التطبيق: اضغط Ctrl+C
echo.
echo ============================================
echo.

wsl bash -c "cd /home/user/duhatv/quran-clean && python app.py"

pause
