# 🎓 Presenze Aula Unical

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema di rilevamento presenze universitarie basato su **QR code dinamici** con token a scadenza temporizzata e validazione server-side.

**Sviluppato da**: [Francesco De Rango](mailto:francesco.derango@unical.it) - Università della Calabria

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

## 📋 Indice

- [Caratteristiche](#-caratteristiche)
- [Come funziona](#-come-funziona)
- [Utilizzo - 3 Modalità](#-utilizzo---3-modalità)
  - [Modalità 1: Usa App Live](#modalità-1-usa-app-live-raccomandato)
  - [Modalità 2: Deploya Tua Versione](#modalità-2-deploya-la-tua-versione)
  - [Modalità 3: Sviluppo Locale](#modalità-3-sviluppo-locale)
- [Architettura e Sicurezza](#-architettura-e-sicurezza)
- [Configurazione](#-configurazione)
- [FAQ](#-faq)
- [Contribuire](#-contribuire)
- [Licenza](#-licenza)

---

## ✨ Caratteristiche

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
┌─────────────┐      ┌──────────────┐      ┌────────────────┐
│   Docente   │      │  QR Dinamico │      │    Studente    │
│             │─────▶│              │─────▶│                │
│ Genera QR   │      │  Token + URL │      │  Scansiona QR  │
└─────────────┘      └──────────────┘      └────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Validazione │
                     │   Server     │
                     └──────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      ✅ Token Valido              ⛔ Token Scaduto
      Redirect a Form              Mostra Errore
```

### Processo dettagliato

1. **Docente**: Inserisce il link del Microsoft Form nella sidebar
2. **Sistema**: Genera un QR code con token calcolato come `floor(timestamp / interval)`
3. **Studente**: Scansiona il QR → viene reindirizzato alla pagina intermedia dell'app
4. **Validazione**: 
   - Se token valido (attuale o precedente) → redirect al form
   - Se token scaduto → mostra messaggio di errore
5. **Auto-refresh**: Il QR si rigenera automaticamente allo scadere dell'intervallo

### Esempio di token

Per intervallo di 60 secondi, alle ore 14:32:45 del 30/09/2025:
```
Token = floor(20250930143245 / 60) = 20250930143200
Validità: 14:32:00 - 14:32:59 + grace period (14:31:00 - 14:31:59)
```

---

## 💻 Utilizzo - 3 Modalità

### Modalità 1: Usa App Live (Raccomandato)

**Per docenti che vogliono usare l'app immediatamente.**

1. **Apri** https://presenze-aula-unical.streamlit.app/
2. **Inserisci** il link del tuo Microsoft Form nella sidebar
3. **Proietta** il QR code in aula
4. **Gli studenti scansionano** e compilano il form

✅ **Nessuna installazione richiesta**  
✅ **Sempre aggiornata**  
✅ **Zero manutenzione**

---

### Modalità 2: Deploya la Tua Versione

**Per altre università/istituzioni che vogliono una propria istanza.**

#### Perché deployare la tua versione?
- Personalizzare dominio/branding
- Controllo completo dell'infrastruttura
- Aggiungere funzionalità custom
- Integrazione con sistemi interni

#### Step-by-step

1. **Fork del repository**
   ```bash
   # Vai su https://github.com/fdr-unical/presenze-aula-unical
   # Click su "Fork" in alto a destra
   ```

2. **Clona il tuo fork**
   ```bash
   git clone https://github.com/TUO-USERNAME/presenze-aula-unical.git
   cd presenze-aula-unical
   ```

3. **Deploy su Streamlit Cloud**
   - Vai su [share.streamlit.io](https://share.streamlit.io)
   - Click **"New app"**
   - Seleziona il tuo repository fork
   - Branch: `main`
   - Main file: `app.py`
   - Click **"Deploy"**

   Il tuo URL sarà: `https://TUO-USERNAME-presenze-aula-unical.streamlit.app/`

4. **Aggiorna BASE_URL nel codice**

   Modifica `app.py` alla riga 24:
   ```python
   # PRIMA:
   BASE_URL = "https://presenze-aula-unical.streamlit.app/"

   # DOPO:
   BASE_URL = "https://TUO-USERNAME-presenze-aula-unical.streamlit.app/"
   ```

5. **Commit e push**
   ```bash
   git add app.py
   git commit -m "Update BASE_URL per la mia istanza"
   git push origin main
   ```

6. **Attendere redeploy** (1-2 minuti)

✅ **Ora hai la tua istanza personalizzata!**

#### Alternative a Streamlit Cloud

L'app può essere deployata anche su:
- **Heroku**: `heroku create` + `git push heroku main`
- **Docker**: Usa il `Dockerfile` incluso
- **Server proprio**: `streamlit run app.py --server.port 8501`

---

### Modalità 3: Sviluppo Locale

**Per sviluppatori che vogliono modificare il codice o contribuire.**

#### Avvio Rapido

**Windows:**
```cmd
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

Gli script gestiscono automaticamente:
- ✅ Verifica Python installato
- ✅ Creazione ambiente virtuale
- ✅ Installazione dipendenze
- ✅ Avvio Streamlit

#### Avvio Manuale

Se preferisci il controllo completo:

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

#### URL Locali

L'app sarà disponibile su:

- **Local URL**: `http://localhost:8501`  
  → Accesso solo dal tuo computer

- **Network URL**: `http://192.168.x.x:8501`  
  → Accesso da altri dispositivi sulla tua rete WiFi/LAN  
  → Utile per testare da smartphone senza deploy

**Nota**: L'IP `192.168.x.x` cambia in base alla tua rete e viene mostrato da Streamlit all'avvio.

#### Test durante sviluppo

Per testare modifiche al codice:

1. Modifica `app.py`
2. Streamlit rileva automaticamente i cambiamenti
3. Click su "Rerun" nel browser per vedere le modifiche

---

## 🔐 Architettura e Sicurezza

### Componenti principali

```python
┌───────────────────────────────────────────────────┐
│                 Streamlit App                      │
├───────────────────────────────────────────────────┤
│  Modalità Docente         │  Modalità Studente    │
│  - Genera QR              │  - Valida token       │
│  - Auto-refresh timer     │  - Redirect sicuro    │
│  - Config UI              │  - Error handling     │
└───────────────────────────────────────────────────┘
         │                           │
         ▼                           ▼
    QR Code Gen               Token Validator
    (qrcode+PIL)             (datetime+floor)
         │                           │
         └───────────┬───────────────┘
                     ▼
            Microsoft Forms
            (forms.office.com)
```

### Misure di sicurezza

- **URL Whitelisting**: Solo domini `forms.office.com` e `forms.microsoft.com` accettati
- **Token temporizzati**: Validità configurabile (30-300 secondi)
- **Grace period**: Accetta anche il token dell'intervallo precedente per sincronizzazione
- **HTML/JS Sanitization**: Double-escape per prevenire XSS
- **No storage**: Nessun dato sensibile memorizzato
- **Server-side validation**: Controllo token lato server, non manipolabile dal client

---

## 📦 Requisiti

### Per usare l'app live
- ✅ Solo un browser moderno (nessuna installazione)

### Per deploy propria versione
- Account GitHub (gratuito)
- Account Streamlit Cloud (gratuito)

### Per sviluppo locale
- Python 3.9 o superiore
- pip (package manager)

#### Dipendenze Python

Vedi [`requirements.txt`](requirements.txt):

```
streamlit>=1.50.0
qrcode[pil]>=7.4.2
validators>=0.20.0
streamlit-autorefresh>=1.0.1
Pillow>=10.0.0
```

---

## ⚙️ Configurazione

### Parametri configurabili in `app.py`

| Parametro | Descrizione | Range | Default |
|-----------|-------------|-------|---------|
| `BASE_URL` | URL pubblico dell'app | String | `https://presenze-aula-unical.streamlit.app/` |
| `ALLOWED_DOMAINS` | Domini consentiti per forms | List | `["forms.office.com", "forms.microsoft.com"]` |
| `DEFAULT_INTERVAL` | Intervallo predefinito (sec) | 30-300 | 60 |
| `MIN_INTERVAL` | Intervallo minimo (sec) | ≥30 | 30 |
| `MAX_INTERVAL` | Intervallo massimo (sec) | ≤300 | 300 |

### Personalizzazioni comuni

#### Aggiungere Google Forms

```python
# In app.py, riga 25
ALLOWED_DOMAINS = [
    "forms.office.com",
    "forms.microsoft.com",
    "docs.google.com"  # ⬅️ Aggiungi questa riga
]
```

#### Modificare intervallo default

```python
# In app.py, riga 26
DEFAULT_INTERVAL = 90  # 90 secondi invece di 60
```

#### Personalizzare tema Streamlit

Modifica `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066CC"      # Colore principale
backgroundColor = "#FFFFFF"    # Sfondo
textColor = "#262730"          # Testo
```

---

## ❓ FAQ

<details>
<summary><strong>Posso usare l'app senza installare nulla?</strong></summary>

Sì! Vai su https://presenze-aula-unical.streamlit.app/ e inizia subito.
</details>

<details>
<summary><strong>Cosa succede se uno studente scansiona un QR scaduto?</strong></summary>

Il sistema mostra: *"⛔ QR scaduto o non valido. Richiedi un nuovo QR al docente."*

Grazie al **grace period**, QR scaduti da meno di un intervallo sono comunque accettati per gestire ritardi di sincronizzazione.
</details>

<details>
<summary><strong>Gli studenti possono condividere il QR via WhatsApp?</strong></summary>

No. Il QR scade dopo pochi secondi (30-300 configurabili) e viene validato server-side. Screenshot o link condivisi dopo la scadenza non funzionano.
</details>

<details>
<summary><strong>Serve un database per salvare le presenze?</strong></summary>

No. L'app genera solo QR temporanei che reindirizzano a Microsoft Forms. Le presenze vengono salvate direttamente da Microsoft Forms nel tuo account Office 365.
</details>

<details>
<summary><strong>Posso usare Google Forms invece di Microsoft Forms?</strong></summary>

Sì, basta aggiungere `"docs.google.com"` alla lista `ALLOWED_DOMAINS` nel codice (vedi [Configurazione](#-configurazione)).
</details>

<details>
<summary><strong>Quanti studenti possono scansionare contemporaneamente?</strong></summary>

Non ci sono limiti tecnici lato app. Il limite dipende dalla capacità di Microsoft Forms di gestire submit simultanei (tipicamente migliaia).
</details>

<details>
<summary><strong>Posso deployare su server mio invece di Streamlit Cloud?</strong></summary>

Sì! L'app è standard Streamlit. Esegui `streamlit run app.py --server.port 8501` su qualsiasi server con Python 3.9+.
</details>

<details>
<summary><strong>Come aggiorno l'app live dopo un push su GitHub?</strong></summary>

Streamlit Cloud monitora il repository. Ogni push su `main` triggera un redeploy automatico (1-2 minuti).
</details>

---

## 🤝 Contribuire

Contributi, segnalazioni bug e richieste di funzionalità sono benvenuti!

### Come contribuire

1. **Fork** il progetto
2. **Crea** un branch per la feature (`git checkout -b feature/NuovaFunzione`)
3. **Commit** le modifiche (`git commit -m 'feat: aggiunge supporto Google Forms'`)
4. **Push** al branch (`git push origin feature/NuovaFunzione`)
5. **Apri** una Pull Request

Vedi [CONTRIBUTING.md](CONTRIBUTING.md) per linee guida dettagliate.

### Segnalare bug

Apri una [Issue](https://github.com/fdr-unical/presenze-aula-unical/issues) descrivendo:
- Comportamento atteso vs osservato
- Step per riprodurre il bug
- Screenshot (se applicabile)
- Ambiente (OS, browser, versione Python)

---

## 📝 Licenza

Questo progetto è rilasciato sotto licenza **MIT License**.

```
Copyright (c) 2025 Francesco De Rango

Permesso concesso di usare, copiare, modificare e distribuire
questo software per qualsiasi scopo, anche commerciale.
```

Vedi il file [LICENSE](LICENSE) per il testo completo.

---

## 🙏 Riconoscimenti

- [Streamlit](https://streamlit.io) - Framework per web app Python
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) - Generazione QR code
- [streamlit-autorefresh](https://github.com/kmcgrady/streamlit-autorefresh) - Componente auto-refresh
- [Microsoft Forms](https://forms.office.com) - Sistema di raccolta dati

---

## 👤 Autore

**Francesco De Rango**  
📧 Email: [francesco.derango@unical.it](mailto:francesco.derango@unical.it)  
🏛️ Università della Calabria  
🔗 GitHub: [https://github.com/fdr-unical/presenze-aula-unical](https://github.com/fdr-unical/presenze-aula-unical)

---

## 📧 Contatti

Per domande, supporto o collaborazioni:
- **Issues**: [https://github.com/fdr-unical/presenze-aula-unical/issues](https://github.com/fdr-unical/presenze-aula-unical/issues)
- **Email**: [francesco.derango@unical.it](mailto:francesco.derango@unical.it)
- **Repository**: [https://github.com/fdr-unical/presenze-aula-unical](https://github.com/fdr-unical/presenze-aula-unical)

---

<p align="center">
  Sviluppato con ❤️ da <a href="mailto:francesco.derango@unical.it">Francesco De Rango</a><br>
  In uso presso <a href="https://www.unical.it">Università della Calabria</a>
</p>
