echo %PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;../functions
echo %PYTHONPATH%
lazydocs.exe --output-path="." --src-base-url="https://github.com/qlefevre/stabilitywarrants/blob/main/" --overview-file="README.md" ../functions