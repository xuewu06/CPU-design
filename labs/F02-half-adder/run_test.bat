@echo off
chcp 65001 >nul
set "LOGISIM=D:\Program Files\logisim-evolution\logisim-evolution.exe"
cd /d "%~dp0"

if not exist "%LOGISIM%" (
  echo [ERROR] Logisim not found at:
  echo   %LOGISIM%
  echo Please edit LOGISIM in this bat file.
  pause
  exit /b 1
)

echo ===== 1. Load circuit (stats) =====
"%LOGISIM%" -o en --no-splash -t stats half_adder.circ
echo.
echo ===== 2. Run test vectors =====
"%LOGISIM%" -o en --no-splash -w main vectors.txt half_adder.circ
echo.
echo Expected result: Passed: 4, Failed: 0
echo.
pause
