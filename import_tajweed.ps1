# Import Tajweed Script
# UTF-8 with BOM

Write-Host "======================================================================"
Write-Host "Import Tajweed Colored Version"
Write-Host "======================================================================"
Write-Host ""

$tajweedFile = "C:\DataB\quran_Ayat\quran_Ayat\quran_text_with_tajweed.json"

if (Test-Path $tajweedFile) {
    Write-Host "File found: quran_text_with_tajweed.json" -ForegroundColor Green
    Write-Host ""
    Write-Host "Importing..." -ForegroundColor Yellow
    Write-Host ""

    python scripts\import_quran_smart.py --file $tajweedFile --version tajweed

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Tajweed imported successfully" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now:" -ForegroundColor Cyan
        Write-Host "   - View colored tajweed in the app" -ForegroundColor White
        Write-Host "   - Switch between different qiraat" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "[ERROR] Tajweed import failed" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] File not found: $tajweedFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please verify the file path" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================"
