# 🎓 Presenze Aula Unical

Sistema di rilevamento presenze universitarie basato su **QR code dinamici** con token a scadenza temporizzata e validazione server-side.

**Sviluppato da**: Francesco De Rango - Università della Calabria

---

## 🚀 Usa Subito (Zero Setup)

L'app è **già online e funzionante**:

🌐 **https://presenze-aula-unical.streamlit.app/**

Ideale per:
- ✅ Docenti che vogliono usare l'app immediatamente
- ✅ Test rapido del sistema
- ✅ Utilizzo quotidiano in aula

**Nessuna installazione richiesta** - apri il link e inizia a generare QR code!

---

## 📋 Caratteristiche

- **🔒 Sicurezza avanzata**: Token temporizzati con grace period per prevenire condivisioni fraudolente
- **⚡ Auto-refresh intelligente**: QR code che si aggiorna automaticamente senza ricaricare la pagina
- **📱 Mobile-first**: Ottimizzato per scansione da smartphone
- **🎯 Validazione URL**: Whitelist integrata per Microsoft Forms
- **📊 Progress bar visuale**: Countdown grafico del tempo rimanente
- **🌐 UTC/Locale**: Supporto fusi orari multipli
- **♿ Accessibile**: Interfaccia user-friendly per docenti e studenti
- **🚀 Zero setup**: Nessun database o autenticazione richiesta

---

## 🔄 Come funziona

### Flusso di lavoro

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐
│   Docente   │───▶│  QR Dinamico │───▶│    Studente    │
│  Genera QR  │    │  Token + URL │    │  Scansiona QR  │
└─────────────┘    └──────────────┘    └────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Validazione │
                     │    Server    │
                     └──────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      ✅ Token Valido            ⛔ Token Scaduto
      Redirect a Form            Mostra Errore
```

### Processo dettagliato

1. **Docente**: Inserisce il link del Microsoft Form nella sidebar
2. **Sistema**: Genera un QR code con token calcolato come `floor(timestamp / interval)`
3. **Studente**: Scansiona il QR → viene reindirizzato alla pagina intermedia dell'app
4. **Validazione**:
   - Se token valido (attuale o precedente) → redirect al form
   - Se token scaduto → mostra messaggio di errore
5. **Auto-refresh**: Il QR si rigenera automaticamente allo scadere dell'intervallo

---

## 💻 Utilizzo

### Modalità 1: Usa App Live (Raccomandato) ⭐

**Per docenti che vogliono usare l'app immediatamente.**

1. **Apri** https://presenze-aula-unical.streamlit.app/
2. **Inserisci** il link del tuo Microsoft Form nella sidebar
3. **Proietta** il QR code in aula
4. **Gli studenti scansionano** e compilano il form

✅ **Nessuna installazione richiesta**  
✅ **Sempre aggiornata**  
✅ **Zero manutenzione**

### Modalità 2: Sviluppo Locale

**Per sviluppatori che vogliono modificare il codice.**

#### Avvio Rapido

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

#### Avvio Manuale

```bash
# 1. Clona il repository
git clone https://github.com/fdr-unical/presenze-aula-unical.git
cd presenze-aula-unical

# 2. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate  # Windows

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Avvia l'app
streamlit run app.py
```

L'app sarà disponibile su:
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://192.168.x.x:8501` (per test da altri dispositivi)

---

## 🔐 Architettura e Sicurezza

### Misure di sicurezza

- **URL Whitelisting**: Solo domini `forms.office.com` e `forms.microsoft.com` accettati
- **Token temporizzati**: Validità configurabile (30-300 secondi)
- **Grace period**: Accetta anche il token dell'intervallo precedente per sincronizzazione
- **Server-side validation**: Controllo token lato server, non manipolabile dal client
- **No storage**: Nessun dato sensibile memorizzato

---

## 📦 Requisiti

### Per usare l'app live
- ✅ Solo un browser moderno (nessuna installazione)

### Per sviluppo locale
- Python 3.9 o superiore
- pip (package manager)

#### Dipendenze Python

Vedi `requirements.txt`:
```
streamlit>=1.50.0
qrcode[pil]>=7.4.2
validators>=0.20.0
streamlit-autorefresh>=1.0.1
Pillow>=10.0.0
```

---

## ⚙️ Configurazione

### Parametri configurabili in app.py

| Parametro | Descrizione | Range | Default |
|-----------|-------------|-------|---------|
| `BASE_URL` | URL pubblico dell'app | String | `https://presenze-aula-unical.streamlit.app/` |
| `ALLOWED_DOMAINS` | Domini consentiti per forms | List | `["forms.office.com", "forms.microsoft.com"]` |
| `DEFAULT_INTERVAL` | Intervallo predefinito (sec) | 30-300 | 60 |
| `MIN_INTERVAL` | Intervallo minimo (sec) | ≥30 | 30 |
| `MAX_INTERVAL` | Intervallo massimo (sec) | ≤300 | 300 |

---

## 🔗 Progetti correlati

- **[qrcode-presenze-unical](https://github.com/fdr-unical/qrcode-presenze-unical)** - Versione HTML standalone (no server richiesto)

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **MIT License**.

```
Copyright (c) 2025 Francesco De Rango

Permesso concesso di usare, copiare, modificare e distribuire
questo software per qualsiasi scopo, anche commerciale.
```

Vedi il file LICENSE per il testo completo.

---

## 👤 Autore

**Francesco De Rango**  
📧 Email: francesco.derango@unical.it  
🏛️ Università della Calabria  
🔗 GitHub: [@fdr-unical](https://github.com/fdr-unical)

---

## 📧 Contatti

Per domande, supporto o collaborazioni:

- **Issues**: https://github.com/fdr-unical/presenze-aula-unical/issues
- **Email**: francesco.derango@unical.it
- **Repository**: https://github.com/fdr-unical/presenze-aula-unical

---

Sviluppato da Francesco De Rango  
In uso presso Università della Calabria
