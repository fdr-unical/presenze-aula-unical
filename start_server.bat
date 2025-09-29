@echo off
REM === Presenze Aula Unical - Avvio automatico ===

echo Aggiornamento pip...
python -m pip install --upgrade pip

echo Installazione dipendenze...
python -m pip install -r requirements.txt

echo Avvio server Streamlit...
python -m streamlit run app.py

pause
