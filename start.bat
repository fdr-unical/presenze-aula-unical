@echo off
REM ============================================================
REM Presenze Aula Unical - Avvio Automatico (Windows)
REM ============================================================

title Presenze Aula Unical

echo.
echo ============================================================
echo   PRESENZE AULA UNICAL - SETUP E AVVIO
echo ============================================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato!
    echo.
    echo Installa Python da: https://www.python.org/downloads/
    echo Assicurati di selezionare "Add Python to PATH" durante l'installazione.
    echo.
    pause
    exit /b 1
)

echo [1/4] Verifica Python...
python --version
echo.

REM Controlla se esiste venv
if not exist "venv" (
    echo [2/4] Creazione ambiente virtuale...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRORE] Impossibile creare ambiente virtuale!
        pause
        exit /b 1
    )
    echo Ambiente virtuale creato con successo.
    echo.
) else (
    echo [2/4] Ambiente virtuale esistente trovato.
    echo.
)

REM Attiva ambiente virtuale
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRORE] Impossibile attivare ambiente virtuale!
    pause
    exit /b 1
)

REM Aggiorna pip
echo [3/4] Aggiornamento pip...
python -m pip install --upgrade pip --quiet
echo.

REM Installa dipendenze
echo [4/4] Installazione/Aggiornamento dipendenze...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERRORE] Errore durante l'installazione delle dipendenze!
    echo.
    echo Prova a installare manualmente con:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo Dipendenze installate con successo.
echo.

echo ============================================================
echo   AVVIO STREAMLIT
echo ============================================================
echo.
echo L'app si aprira automaticamente nel browser predefinito.
echo.
echo App locale disponibile su: http://localhost:8501
echo.
echo Per fermare il server, premi CTRL+C in questa finestra.
echo.
echo ============================================================
echo.

REM Avvia Streamlit
python -m streamlit run app.py

REM Se Streamlit termina
echo.
echo ============================================================
echo Server Streamlit terminato.
echo ============================================================
pause
