# Import All Qiraat Script
# UTF-8 with BOM

Write-Host "======================================================================"
Write-Host "Import 6 Qiraat - Quran Database"
Write-Host "======================================================================"
Write-Host ""

$files = @(
    @{File="hafsData_v2-0.json"; Version="hafs"; Name="Hafs"},
    @{File="warshData_v2-1.json"; Version="warsh"; Name="Warsh"},
    @{File="QalounData_v2-1.json"; Version="qaloon"; Name="Qaloon"},
    @{File="DouriData_v2-0.json"; Version="aldori"; Name="Al-Douri"},
    @{File="SousiData_v2-0.json"; Version="alsosi"; Name="Al-Sousi"},
    @{File="shubaData_v2-0.json"; Version="shobah"; Name="Shubah"}
)

$basePath = "C:\QURAN2\data\sources\quran_Ayat"
$totalFiles = $files.Count
$currentFile = 0

Write-Host "Total files to import: $totalFiles" -ForegroundColor Cyan
Write-Host ""

foreach ($item in $files) {
    $currentFile++
    $filePath = Join-Path $basePath $item.File

    Write-Host "[$currentFile/$totalFiles] Importing: $($item.Name)" -ForegroundColor Yellow

    if (Test-Path $filePath) {
        python scripts\import_quran_smart.py --file $filePath --version $item.Version

        if ($LASTEXITCODE -eq 0) {
            Write-Host "   [OK] $($item.Name) imported successfully" -ForegroundColor Green
        } else {
            Write-Host "   [ERROR] $($item.Name) import failed" -ForegroundColor Red
        }
    } else {
        Write-Host "   [WARNING] File not found: $($item.File)" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "======================================================================"
Write-Host "Import completed!"
Write-Host "======================================================================"
Write-Host ""
Write-Host "Next step: Run the app" -ForegroundColor Cyan
Write-Host "   python app.py" -ForegroundColor White
Write-Host ""
