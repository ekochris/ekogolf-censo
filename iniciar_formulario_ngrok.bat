@echo off
:: Activa el entorno virtual
cd /d "C:\Users\ccarreno\Documents\Proyecto Censo"
call venv\Scripts\activate

:: Establece configuración de Flask
set FLASK_APP=run.py
set FLASK_ENV=development

:: Inicia Flask en el puerto 8080
start "" cmd /k python run.py

:: Espera unos segundos para asegurar que Flask arranque antes de abrir Ngrok
timeout /t 5

:: Agrega authtoken (solo se ejecuta la primera vez, luego lo puedes comentar)
"C:\Users\ccarreno\Documents\Ngrok\ngrok.exe" config add-authtoken 2wYBpZKFulw4Pqe2s128bFfeoJs_3tgoQX7uCws7nZZ25WwbH

:: Inicia Ngrok en el mismo puerto donde corre Flask
start "" cmd /k "C:\Users\ccarreno\Documents\Ngrok\ngrok.exe" http 8080

pause
