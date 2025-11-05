# ===================================
# نسخ بسيط من Windows إلى WSL
# ===================================

Write-Host ""
Write-Host "🚀 بدء النسخ..." -ForegroundColor Cyan
Write-Host ""

# التحقق من WSL
Write-Host "🔍 التحقق من WSL..." -ForegroundColor Yellow
wsl echo "✅ WSL يعمل بشكل صحيح"
Write-Host ""

# إنشاء المجلدات
Write-Host "📁 إنشاء المجلدات..." -ForegroundColor Yellow
wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/data/{ayat,surahs,words,fonts}"
wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/static/fonts"
Write-Host "✅ تم إنشاء المجلدات" -ForegroundColor Green
Write-Host ""

# نسخ جميع الملفات
Write-Host "📦 نسخ الملفات من C:\Qgo3..." -ForegroundColor Yellow
Write-Host ""

# تحويل مسار Windows إلى مسار WSL واستخدام cp
wsl bash -c "cp /mnt/c/Qgo3/*.txt /home/user/duhatv/quran-clean/data/ayat/ 2>/dev/null && echo '  ✓ ملفات TXT' || echo '  ⚠ لم يتم العثور على ملفات TXT'"
wsl bash -c "cp /mnt/c/Qgo3/*.json /home/user/duhatv/quran-clean/data/ayat/ 2>/dev/null && echo '  ✓ ملفات JSON' || echo '  ⚠ لم يتم العثور على ملفات JSON'"
wsl bash -c "cp /mnt/c/Qgo3/*.xlsx /home/user/duhatv/quran-clean/data/surahs/ 2>/dev/null && echo '  ✓ ملف Excel' || echo '  ⚠ لم يتم العثور على ملف Excel'"
wsl bash -c "cp /mnt/c/Qgo3/*.ttf /home/user/duhatv/quran-clean/data/fonts/ 2>/dev/null && echo '  ✓ خطوط TTF' || echo '  ⚠ لم يتم العثور على خطوط TTF'"
wsl bash -c "cp /mnt/c/Qgo3/*.otf /home/user/duhatv/quran-clean/data/fonts/ 2>/dev/null && echo '  ✓ خطوط OTF' || echo '  ⚠ لم يتم العثور على خطوط OTF'"

# نسخ ملفات الكلمات إلى مجلد words
Write-Host ""
Write-Host "📝 نقل ملفات الكلمات..." -ForegroundColor Yellow
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/*word*.txt /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملفات الكلمات TXT'"
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/irab*.json /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملف الإعراب'"
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/sarf*.json /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملف الصرف'"
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/meaning*.json /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملف المعاني'"
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/rasm*.json /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملف الرسم'"
wsl bash -c "mv /home/user/duhatv/quran-clean/data/ayat/statistics*.json /home/user/duhatv/quran-clean/data/words/ 2>/dev/null && echo '  ✓ ملف الإحصائيات'"

# نسخ الخطوط إلى مجلد static
Write-Host ""
Write-Host "🔤 نسخ الخطوط إلى static..." -ForegroundColor Yellow
wsl bash -c "cp /home/user/duhatv/quran-clean/data/fonts/* /home/user/duhatv/quran-clean/static/fonts/ 2>/dev/null && echo '  ✓ تم نسخ الخطوط'"

Write-Host ""
Write-Host "📊 عرض الملفات المنسوخة..." -ForegroundColor Yellow
Write-Host ""
Write-Host "الآيات:" -ForegroundColor Cyan
wsl bash -c "ls -lh /home/user/duhatv/quran-clean/data/ayat/ | grep -E '\.(txt|json)$' | wc -l | xargs echo '  ملفات:'"
Write-Host ""
Write-Host "السور:" -ForegroundColor Cyan
wsl bash -c "ls -lh /home/user/duhatv/quran-clean/data/surahs/ | grep xlsx | wc -l | xargs echo '  ملفات:'"
Write-Host ""
Write-Host "الكلمات:" -ForegroundColor Cyan
wsl bash -c "ls -lh /home/user/duhatv/quran-clean/data/words/ | grep -E '\.(txt|json)$' | wc -l | xargs echo '  ملفات:'"
Write-Host ""
Write-Host "الخطوط:" -ForegroundColor Cyan
wsl bash -c "ls -lh /home/user/duhatv/quran-clean/data/fonts/ | grep -E '\.(ttf|otf)$' | wc -l | xargs echo '  ملفات:'"

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "✅ انتهى النسخ!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "الخطوة التالية:" -ForegroundColor Yellow
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && pip install -r requirements.txt'" -ForegroundColor White
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && python import_data.py'" -ForegroundColor White
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && python app.py'" -ForegroundColor White
Write-Host ""
pause
