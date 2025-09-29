# Presenze Aula Unical

App Streamlit per generare **QR code dinamici** con token a scadenza e verificare lato server che i QR scaduti non funzionino.

---

## ⚙️ Come funziona
- **Docente**: genera un QR che punta alla stessa app (pagina intermedia).
- **Studente**: scansiona il QR → la pagina intermedia verifica che il token sia valido.  
  - Se valido → reindirizza al Microsoft Form.  
  - Se scaduto → mostra errore.  

🔢 Il token è calcolato come timestamp “floorato” all’intervallo scelto (es. 60s → `yyyymmddhhmm00`), così tutti gli studenti vedono lo stesso codice per quel minuto.

---

## 📦 Requisiti
- Python 3.9+  
- Librerie: vedi `requirements.txt`  

---

## ▶️ Avvio locale
```bash
pip install -r requirements.txt
streamlit run app.py
```
Apri nel browser:  
```
http://localhost:8501
```

---

## 🧪 Test locale rapido
1. Inserisci nella sidebar il link al tuo **Microsoft Form**.  
2. L’app userà l’URL pubblico fisso:  
   ```
   https://presenze-aula-unical.streamlit.app/
   ```
3. Abbassa l’intervallo a 10s per vedere il refresh rapido.  
4. Prova ad aprire manualmente un URL come:  
   ```
   https://presenze-aula-unical.streamlit.app/?token=YYYYMMDDhhmmss&to=https://forms.office.com/...&interval=60&utc=0
   ```

---

## 🌐 Deploy su Streamlit Cloud
1. Carica `app.py` e `requirements.txt` su un repository GitHub.  
2. Vai su **Streamlit Cloud** → *New app* → seleziona repo/branch/file `app.py` → *Deploy*.  
3. L’app sarà disponibile al link:  
   ```
   https://presenze-aula-unical.streamlit.app/
   ```

---

## 🔧 Parametri
- **Intervallo (s)**: durata validità token (es. 60).  
- **UTC**: se attivo, usa l’orario UTC (utile se server e docenti sono in fusi orari diversi).  

---

## 📄 Licenza
MIT License — vedi `LICENSE`.
