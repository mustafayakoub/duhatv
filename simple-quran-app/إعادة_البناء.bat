@echo off
chcp 65001 > nul
cls

echo.
echo ════════════════════════════════════════════════════════════════════════
echo                  🌙 إعادة بناء quran_unified.db 🌙
echo ════════════════════════════════════════════════════════════════════════
echo.
echo   من القواعد الموجودة لديك:
echo   ✓ quran_ultimate_final.db
echo   ✓ surah_database_app_v32.db
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

pause

python rebuild_simple.py

echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
pause
