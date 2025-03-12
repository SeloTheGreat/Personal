@echo off

::call pip via python version

if "%1"=="help" goto help
if [%1]==[] goto help

::The %rest% argument contains heading by 1 space after being set! note that
set first=%1
set rest=

shift
:sloop
if [%1]==[] goto eloop
set rest=%rest% %1
shift
goto sloop
:eloop

if exist %USERPROFILE%\AppData\Local\Programs\Python\Python%first%\ (
	%USERPROFILE%\AppData\Local\Programs\Python\Python%first%\Scripts\pip%rest%
) else (
	echo [EXITING]: First argument must be empty or an avaliable python version that exists on your system & exit /b
)

exit /b

:help
echo [HELP]:
echo First argument must be empty or an avaliable python version that exists on your system.
echo Via the first argument, the appropariate version of pythons pip will be executed with the rest of the arguments
echo 'vpip 39 --version' : this will display the version of pip within python 3.9
exit /b