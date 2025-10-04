@echo off
echo ============================================
echo Presenze Aula UnICal - Streamlit App
echo ============================================
echo.

REM Verifica Python installato
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Python non trovato!
    echo.
    echo Scarica Python da: https://www.python.org/downloads/
    echo Assicurati di selezionare "Add Python to PATH" durante l'installazione
    pause
    exit /b 1
)

echo [1/4] Verifica Python... OK
python --version

REM Crea ambiente virtuale se non esiste
if not exist "venv" (
    echo.
    echo [2/4] Creazione ambiente virtuale...
    python -m venv venv
    echo Ambiente virtuale creato!
) else (
    echo.
    echo [2/4] Ambiente virtuale già esistente... OK
)

REM Attiva ambiente virtuale
echo.
echo [3/4] Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

REM Installa dipendenze
echo.
echo [4/4] Installazione dipendenze...
pip install -r requirements.txt

REM Avvia Streamlit
echo.
echo ============================================
echo Avvio Streamlit...
echo ============================================
echo.
streamlit run app.py

pause
