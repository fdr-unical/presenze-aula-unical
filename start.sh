#!/bin/bash

# ============================================================
# Presenze Aula Unical - Avvio Automatico (Linux/macOS)
# ============================================================

echo ""
echo "============================================================"
echo "  PRESENZE AULA UNICAL - SETUP E AVVIO"
echo "============================================================"
echo ""

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python 3 non trovato!"
    echo ""
    echo "Installa Python 3:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  - macOS: brew install python3"
    echo ""
    exit 1
fi

echo "[1/4] Verifica Python..."
python3 --version
echo ""

# Controlla se esiste venv
if [ ! -d "venv" ]; then
    echo "[2/4] Creazione ambiente virtuale..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERRORE] Impossibile creare ambiente virtuale!"
        exit 1
    fi
    echo "Ambiente virtuale creato con successo."
    echo ""
else
    echo "[2/4] Ambiente virtuale esistente trovato."
    echo ""
fi

echo "Attivazione ambiente virtuale..."
source venv/bin/activate

echo "[3/4] Aggiornamento pip..."
python -m pip install --upgrade pip --quiet
echo ""

echo "[4/4] Installazione/Aggiornamento dipendenze..."
pip install -r requirements.txt --quiet
echo "Dipendenze installate con successo."
echo ""

echo "============================================================"
echo "  AVVIO STREAMLIT"
echo "============================================================"
echo ""
echo "L'app si aprira automaticamente nel browser predefinito."
echo ""
echo "App locale disponibile su: http://localhost:8501"
echo ""
echo "Per fermare il server, premi CTRL+C in questo terminale."
echo ""
echo "============================================================"
echo ""

python -m streamlit run app.py

echo ""
echo "============================================================"
echo "Server Streamlit terminato."
echo "============================================================"
