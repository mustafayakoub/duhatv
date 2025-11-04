# سكريبت استيراد نسخة التجويد الملون
# Import Tajweed Colored Version

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🎨 استيراد نسخة التجويد الملون" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$tajweedFile = "C:\DataB\quran_Ayat\quran_Ayat\quran_text_with_tajweed.json"

if (Test-Path $tajweedFile) {
    Write-Host "📁 الملف موجود: quran_text_with_tajweed.json" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔄 جاري الاستيراد..." -ForegroundColor Yellow
    Write-Host ""

    # استيراد التجويد
    python scripts\import_quran_smart.py --file $tajweedFile --version tajweed

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ نجح استيراد نسخة التجويد الملون" -ForegroundColor Green
        Write-Host ""
        Write-Host "💡 الآن يمكنك:" -ForegroundColor Cyan
        Write-Host "   - عرض التجويد الملون في التطبيق" -ForegroundColor White
        Write-Host "   - التبديل بين القراءات المختلفة" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "❌ فشل استيراد نسخة التجويد" -ForegroundColor Red
    }
} else {
    Write-Host "❌ الملف غير موجود: $tajweedFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 تأكد من المسار الصحيح" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
