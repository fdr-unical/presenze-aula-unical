# 🚀 Quick Start

Guida rapida per iniziare a usare Presenze Aula Unical.

---

## 🌐 Opzione 1: Usa App Live (Zero Setup)

**Modo più semplice e veloce!**

1. Apri **https://presenze-aula-unical.streamlit.app/**
2. Inserisci il link del tuo Microsoft Form
3. Proietta il QR code
4. Gli studenti scansionano

✅ **Nessuna installazione richiesta**

---

## 💻 Opzione 2: Avvio Locale (Per Sviluppatori)

### Windows

**Doppio click su** `start.bat`

### Linux/macOS

```bash
chmod +x start.sh
./start.sh
```

L'app si aprirà automaticamente su `http://localhost:8501`

---

## 🔧 Cosa fanno gli script?

Gli script automatizzano:

1. ✅ Verifica installazione Python
2. ✅ Creazione ambiente virtuale (se non esiste)
3. ✅ Installazione/aggiornamento dipendenze
4. ✅ Avvio server Streamlit

---

## 📖 Avvio Manuale (Alternativo)

Se preferisci controllare ogni step:

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ Problemi Comuni

### "Python non trovato"
Installa Python 3.9+ da [python.org](https://www.python.org/downloads/)

**Windows**: Seleziona "Add Python to PATH" durante l'installazione.

### "Errore durante installazione dipendenze"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Porta 8501 già in uso
```bash
streamlit run app.py --server.port 8502
```

---

## 🛑 Fermare il Server

Premi **CTRL+C** nella finestra del terminale/prompt.

---

## 📚 Documentazione Completa

Vedi [README.md](README.md) per:
- Architettura e sicurezza
- Deploy di una tua versione
- Configurazione avanzata
- FAQ complete
