# ===================================
# نسخ الملفات من Windows إلى WSL
# ===================================

Write-Host "🚀 بدء نسخ الملفات..." -ForegroundColor Cyan
Write-Host ""

# التأكد من وجود المجلد المصدر
if (-Not (Test-Path "C:\Qgo3")) {
    Write-Host "❌ المجلد C:\Qgo3 غير موجود!" -ForegroundColor Red
    Write-Host "الرجاء التأكد من مسار الملفات" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ تم العثور على المجلد: C:\Qgo3" -ForegroundColor Green
Write-Host ""

# 1. نسخ ملفات الآيات
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

$count = 0
foreach ($file in $ayatFiles) {
    $sourcePath = "C:\Qgo3\$file"
    if (Test-Path $sourcePath) {
        # نسخ مباشر إلى WSL
        wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/data/ayat"
        $content = Get-Content -Path $sourcePath -Raw -Encoding UTF8
        $tempFile = [System.IO.Path]::GetTempFileName()
        Set-Content -Path $tempFile -Value $content -Encoding UTF8
        wsl bash -c "cat '$($tempFile -replace '\\', '/')' > /home/user/duhatv/quran-clean/data/ayat/$file"
        Remove-Item $tempFile
        Write-Host "  ✓ $file" -ForegroundColor Green
        $count++
    } else {
        Write-Host "  ⚠ غير موجود: $file" -ForegroundColor DarkYellow
    }
}
Write-Host "  تم نسخ $count ملف" -ForegroundColor Cyan
Write-Host ""

# 2. نسخ ملف السور
Write-Host "2️⃣  نسخ ملف السور..." -ForegroundColor Yellow
$surahFile = "C:\Qgo3\suar_quran_Mustafa_Yakoub.xlsx"
if (Test-Path $surahFile) {
    wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/data/surahs"
    $bytes = [System.IO.File]::ReadAllBytes($surahFile)
    $base64 = [System.Convert]::ToBase64String($bytes)
    wsl bash -c "echo '$base64' | base64 -d > /home/user/duhatv/quran-clean/data/surahs/suar_quran_Mustafa_Yakoub.xlsx"
    Write-Host "  ✓ suar_quran_Mustafa_Yakoub.xlsx" -ForegroundColor Green
} else {
    Write-Host "  ❌ ملف السور غير موجود!" -ForegroundColor Red
}
Write-Host ""

# 3. نسخ ملفات الكلمات
Write-Host "3️⃣  نسخ ملفات الكلمات..." -ForegroundColor Yellow

$wordFiles = @(
    "quran_word Mustafa_Y2.txt",
    "irab_quran.json",
    "sarf_quran.json",
    "meaning_quran.json",
    "rasm_quran.json",
    "statistics_quran.json"
)

$count = 0
foreach ($file in $wordFiles) {
    $sourcePath = "C:\Qgo3\$file"
    if (Test-Path $sourcePath) {
        wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/data/words"
        $content = Get-Content -Path $sourcePath -Raw -Encoding UTF8
        $tempFile = [System.IO.Path]::GetTempFileName()
        Set-Content -Path $tempFile -Value $content -Encoding UTF8 -NoNewline
        wsl bash -c "cat '$($tempFile -replace '\\', '/')' > /home/user/duhatv/quran-clean/data/words/$file"
        Remove-Item $tempFile
        Write-Host "  ✓ $file" -ForegroundColor Green
        $count++
    } else {
        Write-Host "  ⚠ غير موجود: $file" -ForegroundColor DarkYellow
    }
}
Write-Host "  تم نسخ $count ملف" -ForegroundColor Cyan
Write-Host ""

# 4. نسخ الخطوط
Write-Host "4️⃣  نسخ الخطوط..." -ForegroundColor Yellow
wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/data/fonts"
wsl bash -c "mkdir -p /home/user/duhatv/quran-clean/static/fonts"

$fonts = Get-ChildItem -Path "C:\Qgo3" -Include *.ttf,*.otf,*.woff,*.woff2 -Recurse -ErrorAction SilentlyContinue
$count = 0
foreach ($font in $fonts) {
    $bytes = [System.IO.File]::ReadAllBytes($font.FullName)
    $base64 = [System.Convert]::ToBase64String($bytes)
    wsl bash -c "echo '$base64' | base64 -d > /home/user/duhatv/quran-clean/data/fonts/$($font.Name)"
    wsl bash -c "echo '$base64' | base64 -d > /home/user/duhatv/quran-clean/static/fonts/$($font.Name)"
    Write-Host "  ✓ $($font.Name)" -ForegroundColor Green
    $count++
}
Write-Host "  تم نسخ $count خط" -ForegroundColor Cyan
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
