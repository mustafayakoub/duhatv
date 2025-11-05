@echo off
chcp 65001 > nul
echo.
echo ========================================
echo    نسخ ملفات البيانات - بسيط وسريع
echo ========================================
echo.

set SOURCE=\\wsl.localhost\Ubuntu\home\quran27\duhatv\data
set DEST=\\wsl.localhost\Ubuntu\home\user\duhatv\quran-clean\data

echo المصدر: %SOURCE%
echo الهدف: %DEST%
echo.
echo جارٍ النسخ...
echo.

robocopy "%SOURCE%\ayat" "%DEST%\ayat" /E /Z /R:3 /W:5
if %ERRORLEVEL% LEQ 7 echo ✓ تم نسخ ayat

robocopy "%SOURCE%\surahs" "%DEST%\surahs" /E /Z /R:3 /W:5
if %ERRORLEVEL% LEQ 7 echo ✓ تم نسخ surahs

robocopy "%SOURCE%\words" "%DEST%\words" /E /Z /R:3 /W:5
if %ERRORLEVEL% LEQ 7 echo ✓ تم نسخ words

robocopy "%SOURCE%\fonts" "%DEST%\fonts" /E /Z /R:3 /W:5
if %ERRORLEVEL% LEQ 7 echo ✓ تم نسخ fonts

robocopy "%DEST%\fonts" "\\wsl.localhost\Ubuntu\home\user\duhatv\quran-clean\static\fonts" /E /Z /R:3 /W:5
if %ERRORLEVEL% LEQ 7 echo ✓ تم نسخ fonts إلى static

echo.
echo ========================================
echo ✅ انتهى النسخ!
echo ========================================
echo.
echo الآن شغّل:
echo   wsl bash -c "cd /home/user/duhatv/quran-clean && pip install -r requirements.txt"
echo   wsl bash -c "cd /home/user/duhatv/quran-clean && python import_data.py"
echo   wsl bash -c "cd /home/user/duhatv/quran-clean && python app.py"
echo.
pause
