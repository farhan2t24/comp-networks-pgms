@echo off
SET PYTHON_PATH="%~dp0.venv\Scripts\python.exe"
SET SERVICE_SCRIPT="%~dp0service_wrapper.py"

if "%1"=="install" (
    %PYTHON_PATH% %SERVICE_SCRIPT% install
    echo Service installed successfully!
    echo To start the service, run: manage_service.bat start
) else if "%1"=="start" (
    net start MessagingService
    echo Service started! Access the app at:
    echo http://localhost:5000 (from this computer^)
    echo http://192.168.0.102:5000 (from other devices on the network^)
) else if "%1"=="stop" (
    net stop MessagingService
    echo Service stopped!
) else if "%1"=="remove" (
    %PYTHON_PATH% %SERVICE_SCRIPT% remove
    echo Service removed!
) else (
    echo Usage:
    echo manage_service.bat install - Install the service
    echo manage_service.bat start   - Start the service
    echo manage_service.bat stop    - Stop the service
    echo manage_service.bat remove  - Remove the service
)