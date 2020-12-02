@echo off
setlocal

echo.
echo [96m Installing PIP[0m
echo [96m----------------[0m
echo.
python requirements\get-pip.py
echo.

echo [96m Installing required packages[0m
echo [96m-----------------------------[0m
echo.
python -m pip install -r requirements.txt
python -m pip install requirements\confluent_kafka-1.2.2rc1-cp35-cp35m-win32.whl
python -m pip install requirements\confluent_kafka-1.2.2rc1-cp35-cp35m-win_amd64.whl
echo.

echo [96m Creating required directories[0m
echo [96m-----------------------------[0m
echo.
mkdir \Logs
echo.

echo [96m Choose modules to be installed[0m
echo [96m--------------------------------[0m
echo.
set /P db_scanner="Database Scanner (y/n): "
set /P kafka_scanner="Kafka Scanner (y/n): "
echo.

echo [96m Configuring setup variables[0m
echo [96m----------------------------[0m
echo.
del modules\settings.py
type nul > modules\settings.py
echo.
python modules\configure\call_server.py
echo.
:Install
requirements\nssm.exe install CallServer python call_server.py
requirements\nssm.exe set CallServer AppDirectory %cd%
requirements\nssm.exe set CallServer AppStdout C:\Logs\call_server.log
requirements\nssm.exe set CallServer AppStderr C:\Logs\call_server.log
requirements\nssm.exe start CallServer
echo.
echo Your call server should now be accessible at http://YOUR_URL:YOUR_PORT/play. Please verify this before continuing.
set /P accessible="Is it accessible? (y/n): "
if "%accessible%" == "n" goto Remove
if "%accessible%" == "N" goto Remove
echo.
python modules\configure\active_directory.py
echo.
python modules\configure\twilio_details.py
echo.
set install=false
set /P password="Please enter your administrator password: "
for /F "tokens=*" %%g in ('whoami') do (SET user=%%g)
if "%kafka_scanner%" == "y" set install=true
if "%kafka_scanner%" == "Y" set install=true
if "%install%" == "true" (
    python modules\configure\kafka_scanner.py
    requirements\nssm.exe install KafkaServer python kafka_scanner.py
    requirements\nssm.exe set KafkaServer AppDirectory %cd%
    requirements\nssm.exe set KafkaServer AppStdout C:\Logs\kafka_scanner.log
    requirements\nssm.exe set KafkaServer AppStderr C:\Logs\kafka_scanner.log
    requirements\nssm.exe set KafkaServer ObjectName %user% %password%
    requirements\nssm.exe start KafkaServer
    echo.
)
set install=false
if "%db_scanner%" == "y" set install=true
if "%db_scanner%" == "Y" set install=true
if "%install%" == "true" (
    python modules\configure\db_connection.py
    requirements\nssm.exe install DBScanner python db_scanner.py
    requirements\nssm.exe set DBScanner AppDirectory %cd%
    requirements\nssm.exe set DBScanner AppStdout C:\Logs\db_scanner.log
    requirements\nssm.exe set DBScanner AppStderr C:\Logs\db_scanner.log
    requirements\nssm.exe set DBScanner ObjectName %user% %password%
    requirements\nssm.exe start DBScanner
    echo.
)
goto End
:Remove
SC Stop CallServer
timeout 3 > NUL
SC Delete CallServer
del modules\settings.py
type nul > modules\settings.py
goto Install
:End
pause