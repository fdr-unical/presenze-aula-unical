#!/bin/bash

echo "============================================"
echo "Presenze Aula UnICal - Streamlit App"
echo "============================================"
echo ""

# Verifica Python installato
if ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python 3 non trovato!"
    echo ""
    echo "Installa Python 3:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  - Fedora/RHEL: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "[1/4] Verifica Python... OK"
python3 --version

# Crea ambiente virtuale se non esiste
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/4] Creazione ambiente virtuale..."
    python3 -m venv venv
    echo "Ambiente virtuale creato!"
else
    echo ""
    echo "[2/4] Ambiente virtuale già esistente... OK"
fi

# Attiva ambiente virtuale
echo ""
echo "[3/4] Attivazione ambiente virtuale..."
source venv/bin/activate

# Installa dipendenze
echo ""
echo "[4/4] Installazione dipendenze..."
pip install -r requirements.txt

# Avvia Streamlit
echo ""
echo "============================================"
echo "Avvio Streamlit..."
echo "============================================"
echo ""
streamlit run app.py
