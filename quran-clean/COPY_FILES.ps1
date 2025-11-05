# سكريبت نسخ ملفات المشروع
# Script to copy all data files to quran-clean project

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "   نسخ ملفات البيانات للمشروع" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# المسار الأصلي للملفات
$sourceDir = "C:\Qgo3"
# مسار المشروع في WSL
$destDir = "\\wsl$\Ubuntu\home\user\duhatv\quran-clean\data"

# التحقق من وجود المجلد الأصلي
if (-Not (Test-Path $sourceDir)) {
    Write-Host "❌ خطأ: المجلد $sourceDir غير موجود" -ForegroundColor Red
    Write-Host "الرجاء التأكد من وجود الملفات في C:\Qgo3\" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ تم العثور على المجلد الأصلي: $sourceDir" -ForegroundColor Green

# إنشاء المجلدات إذا لم تكن موجودة
$folders = @("ayat", "surahs", "words", "fonts")
foreach ($folder in $folders) {
    $path = "$destDir\$folder"
    if (-Not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "📁 تم إنشاء المجلد: $folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📋 بدء نسخ الملفات..." -ForegroundColor Cyan
Write-Host ""

# نسخ ملفات الآيات (18 ملف)
Write-Host "1️⃣  نسخ ملفات الآيات..." -ForegroundColor Yellow
$ayatFiles = @(
    "AlAWWal.txt",
    "hafsData_v2-0.json",
    "warshData_v2-1.json",
    "qalonData_v2-0.json",
    "douriData_v2-0.json",
    "shubaData_v2-0.json",
    "sousiData_v2-0.json",
    "quran-simple-plain_-Mushakkal_v2.txt",
    "quran-simple-plain_-Mushakkal_Fasel.txt",
    "quran-simple-plain_-Mushakkal_Tam.txt",
    "quran-uthmani-min_No_Mushakkel.txt",
    "Transliteration_Latin.txt",
    "quran-simple-plain_-Mushakkal_Tam_Y_END.txt",
    "quran-uthmani_Easy-read_Tashkeel_OFF.txt",
    "quran-uthmani_Easy-read_Tashkeel_Tanween_OFF.txt",
    "quran-uthmani_Easy-read_Tashkeel_tanween_harakat_OFF.txt",
    "quran-uthmani_With_pause_marks.txt",
    "quran-uthmani_With_Tajweed_colors_No_tatweel.txt"
)

$copiedCount = 0
foreach ($file in $ayatFiles) {
    $sourcePath = "$sourceDir\$file"
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination "$destDir\ayat\" -Force
        Write-Host "  ✓ تم نسخ: $file" -ForegroundColor Green
        $copiedCount++
    } else {
        Write-Host "  ⚠ غير موجود: $file" -ForegroundColor DarkYellow
    }
}
Write-Host "  نُسخ $copiedCount ملف من أصل $($ayatFiles.Count)" -ForegroundColor Cyan
Write-Host ""

# نسخ ملف السور (Excel)
Write-Host "2️⃣  نسخ ملف السور..." -ForegroundColor Yellow
$surahFile = "$sourceDir\suar_quran_Mustafa_Yakoub.xlsx"
if (Test-Path $surahFile) {
    Copy-Item -Path $surahFile -Destination "$destDir\surahs\" -Force
    Write-Host "  ✓ تم نسخ: suar_quran_Mustafa_Yakoub.xlsx" -ForegroundColor Green
} else {
    Write-Host "  ❌ ملف السور غير موجود!" -ForegroundColor Red
}
Write-Host ""

# نسخ ملفات الكلمات (6 ملفات JSON)
Write-Host "3️⃣  نسخ ملفات الكلمات..." -ForegroundColor Yellow
$wordFiles = @(
    "quran_word Mustafa_Y2.txt",
    "irab_quran.json",
    "sarf_quran.json",
    "meaning_quran.json",
    "rasm_quran.json",
    "statistics_quran.json"
)

$copiedCount = 0
foreach ($file in $wordFiles) {
    $sourcePath = "$sourceDir\$file"
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination "$destDir\words\" -Force
        Write-Host "  ✓ تم نسخ: $file" -ForegroundColor Green
        $copiedCount++
    } else {
        Write-Host "  ⚠ غير موجود: $file" -ForegroundColor DarkYellow
    }
}
Write-Host "  نُسخ $copiedCount ملف من أصل $($wordFiles.Count)" -ForegroundColor Cyan
Write-Host ""

# نسخ الخطوط (16 ملف)
Write-Host "4️⃣  نسخ الخطوط..." -ForegroundColor Yellow
$fontExtensions = @("*.ttf", "*.otf", "*.woff", "*.woff2")
$copiedCount = 0

foreach ($ext in $fontExtensions) {
    $fonts = Get-ChildItem -Path $sourceDir -Filter $ext -ErrorAction SilentlyContinue
    foreach ($font in $fonts) {
        Copy-Item -Path $font.FullName -Destination "$destDir\fonts\" -Force
        Write-Host "  ✓ تم نسخ: $($font.Name)" -ForegroundColor Green
        $copiedCount++
    }
}

if ($copiedCount -gt 0) {
    Write-Host "  نُسخ $copiedCount خط" -ForegroundColor Cyan
} else {
    Write-Host "  ⚠ لم يتم العثور على خطوط" -ForegroundColor DarkYellow
}
Write-Host ""

# نسخ الخطوط إلى مجلد static أيضاً
Write-Host "5️⃣  نسخ الخطوط إلى مجلد static..." -ForegroundColor Yellow
$staticFontsDir = "\\wsl$\Ubuntu\home\user\duhatv\quran-clean\static\fonts"
if (-Not (Test-Path $staticFontsDir)) {
    New-Item -ItemType Directory -Path $staticFontsDir -Force | Out-Null
}

$fonts = Get-ChildItem -Path "$destDir\fonts\*" -ErrorAction SilentlyContinue
foreach ($font in $fonts) {
    Copy-Item -Path $font.FullName -Destination $staticFontsDir -Force
}
Write-Host "  ✓ تم نسخ الخطوط إلى مجلد static" -ForegroundColor Green
Write-Host ""

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "✅ انتهى نسخ الملفات!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "الخطوة التالية:" -ForegroundColor Yellow
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && pip install -r requirements.txt'" -ForegroundColor White
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && python import_data.py'" -ForegroundColor White
Write-Host "  wsl bash -c 'cd /home/user/duhatv/quran-clean && python app.py'" -ForegroundColor White
Write-Host ""
pause
