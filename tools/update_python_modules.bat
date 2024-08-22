@echo off
if exist ..\..\python_embeded\ (
	echo Update python modules.
	pause
	..\..\python_embeded\python.exe -m pip install -r ..\requirements_versions.txt
	echo Done.
) else (
	echo Can not find python_embeded folder.
)
pause
