@ECHO OFF
ECHO PageHeap Enable / Diable Batch Script - Please run as admin
set /p Choice=Want to Enable or Disable PageHeap? (e or d):%=%
set /p procName=Enter Process Name(Ex. iexplorer.exe):%=%

if "%Choice%"=="e" goto :ENABLE
if "%Choice%"=="d" goto :DISABLE

:ENABLE
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /p /enable %procName%  /full
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /i %procName% +hpa
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /i %procName% +02000000
	goto :EOF
:DISABLE
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /p /disable %procName%  /full
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /i %procName% -hpa
	"C:\Program Files\Debugging Tools for Windows (x86)\gflags.exe" /i %procName% -02000000
	goto :EOF