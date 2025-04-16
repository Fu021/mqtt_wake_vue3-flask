set SCRIPT_DIR=%~dp0
start cmd /k D:\ProgramData\anaconda3\python.exe "%SCRIPT_DIR%/backend/main.py"
start cmd /k npx http-server "%SCRIPT_DIR%/frontend/mqtt_wake/dist"