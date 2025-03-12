@echo off

if "%1"=="help" goto help

set from_dir=%cd%\.cmds
set cmd_dir=

if exist %USERPROFILE%\.cmds\ (
	set cmd_dir=%USERPROFILE%\.cmds
) else (
	mkdir %USERPROFILE%\.cmds
	set cmd_dir=%USERPROFILE%\.cmds
	echo Created folder %cmd_dir%
)

echo %PATH% |find "%cmd_dir%" > nul
if not errorlevel 1 goto placefiles

echo Creating new registry for User enviroment variable, Path

::Safe SETX by https://stackoverflow.com/questions/9546324/adding-a-directory-to-the-path-environment-variable-in-windows/41379378#41379378
set key="HKCU\Environment"
for /F "usebackq tokens=2*" %%A in (`REG QUERY %key% /v PATH`) do set curr_path=%%B
echo %curr_path% > user_path_bak.txt
echo Created new User Path backup file at relative location "%cd%\user_path_bak.txt"
echo If anything unfavorable happens, please refer to this file to manually restore the original User specific Path
setx PATH "%curr_path%";%cmd_dir%

echo Created new registry for User enviroment variable, Path

:placefiles
echo Placing files into %cmd_dir%

for %%f in (%from_dir%\*.*) do (
  if not exist "%cmd_dir%\%%~nxf" (copy "%%f" "%cmd_dir%\%%~nxf")
)

pause
exit /b

:help
echo Sets up all command files withing the working directiory\.cmds
echo Changes User enviroment variable Path if necessary, a backup file is created at the working directory when this happens if the user wants to go back
exit /b