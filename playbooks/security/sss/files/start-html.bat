@echo off
setlocal
rem Nur fuer diesen Prozess; keine dauerhafte ExecutionPolicy-Aenderung.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-html.ps1" %*
set "sss_result=%ERRORLEVEL%"
if not "%sss_result%"=="0" (
  echo.
  echo Start beendet oder Vorbereitung erforderlich. Hinweise oben lesen.
  pause
)
exit /b %sss_result%
