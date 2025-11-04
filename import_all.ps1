# سكريبت استيراد جميع القراءات
# Import All Qira'at Script

Write-Host "=" * 70 -ForegroundColor Green
Write-Host "🚀 استيراد القرآن الكامل - 6 قراءات" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""

# قائمة الملفات مع أنواعها
$files = @(
    @{File="hafsData_v2-0.json"; Version="hafs"; Name="حفص عن عاصم"},
    @{File="warshData_v2-1.json"; Version="warsh"; Name="ورش عن نافع"},
    @{File="QalounData_v2-1.json"; Version="qaloon"; Name="قالون عن نافع"},
    @{File="DouriData_v2-0.json"; Version="aldori"; Name="الدوري عن أبي عمرو"},
    @{File="SousiData_v2-0.json"; Version="alsosi"; Name="السوسي عن أبي عمرو"},
    @{File="shubaData_v2-0.json"; Version="shobah"; Name="شعبة عن عاصم"}
)

$basePath = "C:\QURAN2\data\sources\quran_Ayat"
$totalFiles = $files.Count
$currentFile = 0

Write-Host "📊 سيتم استيراد $totalFiles قراءة مختلفة" -ForegroundColor Cyan
Write-Host ""

foreach ($item in $files) {
    $currentFile++
    $filePath = Join-Path $basePath $item.File

    Write-Host "[$currentFile/$totalFiles] استيراد: $($item.Name)" -ForegroundColor Yellow

    if (Test-Path $filePath) {
        # استيراد الملف
        python scripts\import_quran_smart.py --file $filePath --version $item.Version

        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ نجح استيراد $($item.Name)" -ForegroundColor Green
        } else {
            Write-Host "   ❌ فشل استيراد $($item.Name)" -ForegroundColor Red
        }
    } else {
        Write-Host "   ⚠️  الملف غير موجود: $($item.File)" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "=" * 70 -ForegroundColor Green
Write-Host "✅ اكتمل الاستيراد!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "💡 الآن شغّل التطبيق:" -ForegroundColor Cyan
Write-Host "   python app.py" -ForegroundColor White
Write-Host ""
