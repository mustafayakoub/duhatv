@echo off
chcp 65001 > nul
cls

echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo          🌙 سحب آخر التحديثات من Git
echo          Pull Latest Updates from Git
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

echo 📍 المسار الحالي:
cd
echo.

echo 🔍 التحقق من حالة Git...
git status
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📥 بدء سحب التحديثات...
echo.

git pull origin claude/multilingual-programming-setup-011CUhD7ZhvWxnVqEUQ9rTsR

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

if %ERRORLEVEL% EQU 0 (
    echo ✅ تم سحب التحديثات بنجاح!
    echo.
    echo 📂 الملفات الجديدة:
    echo    ✓ migrate_words_smart.py
    echo    ✓ كيفية_النقل.txt
    echo    ✓ SUMMARY.md
    echo.
    echo 🚀 يمكنك الآن تشغيل:
    echo    python migrate_words_smart.py
) else (
    echo.
    echo ❌ حدث خطأ في السحب!
    echo.
    echo 💡 الحلول الممكنة:
    echo    1. تأكد أنك في مجلد المشروع الصحيح
    echo    2. تأكد من اتصالك بالإنترنت
    echo    3. جرب الطريقة اليدوية أدناه
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo.
pause
