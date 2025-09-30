# 🎓 Presenze Aula Unical

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema di rilevamento presenze universitarie basato su **QR code dinamici** con token a scadenza temporizzata e validazione server-side.

🔗 **Live App**: [https://presenze-aula-unical.streamlit.app/](https://presenze-aula-unical.streamlit.app/)

---

## 📋 Indice

- [Caratteristiche](#-caratteristiche)
- [Come funziona](#-come-funziona)
- [Architettura e Sicurezza](#-architettura-e-sicurezza)
- [Requisiti](#-requisiti)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Deploy su Streamlit Cloud](#-deploy-su-streamlit-cloud)
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

### Software
- Python 3.9 o superiore
- pip (package manager)
- Browser moderno (Chrome, Firefox, Safari, Edge)

### Dipendenze Python
Vedi [`requirements.txt`](requirements.txt) per la lista completa:

```
streamlit>=1.50.0
qrcode[pil]>=7.4.2
validators>=0.20.0
streamlit-autorefresh>=1.0.1
Pillow>=10.0.0
```

---

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/fdr-unical/presenze-aula-unical.git
cd presenze-aula-unical
```

### 2. Crea ambiente virtuale (opzionale ma raccomandato)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installa dipendenze

```bash
pip install -r requirements.txt
```

### 4. Verifica installazione

```bash
streamlit --version
python -c "import qrcode, validators, streamlit_autorefresh; print('OK')"
```

---

## 💻 Utilizzo

### Avvio locale

```bash
streamlit run app.py
```

L'app sarà disponibile su:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Modalità Docente

1. **Apri l'app** nel browser
2. **Inserisci nella sidebar**:
   - Link del Microsoft Form (es. `https://forms.office.com/r/xxxxx`)
   - Intervallo di validità (30-300 secondi, default 60)
   - Timezone (UTC o locale)
3. **Proietta il QR** in aula o condividilo sullo schermo
4. **Il QR si aggiorna automaticamente** allo scadere dell'intervallo

### Modalità Studente

1. **Scansiona il QR** con la fotocamera dello smartphone
2. **Attendi il redirect** automatico
3. **Compila il Microsoft Form** entro il tempo indicato

### Test rapido in locale

Per testare il funzionamento senza studenti:

1. Imposta intervallo a **30 secondi**
2. Genera il QR
3. Copia l'URL sotto il QR (click destro → Copia indirizzo link)
4. Apri l'URL in una nuova tab: 
   - ✅ Se entro 30 secondi → redirect al form
   - ⛔ Se dopo 30 secondi → errore "QR scaduto"

---

## ☁️ Deploy su Streamlit Cloud

### Prerequisiti
- Account GitHub (gratuito)
- Account Streamlit Cloud (gratuito): [streamlit.io/cloud](https://streamlit.io/cloud)

### Step-by-step

1. **Il repository è già su GitHub**:
   ```
   https://github.com/fdr-unical/presenze-aula-unical
   ```

2. **Deploy su Streamlit Cloud**:
   - Vai su [share.streamlit.io](https://share.streamlit.io)
   - Click **"New app"**
   - Seleziona:
     - Repository: `fdr-unical/presenze-aula-unical`
     - Branch: `main`
     - Main file path: `app.py`
   - Click **"Deploy"**

3. **URL pubblico**:
   ```
   https://presenze-aula-unical.streamlit.app/
   ```

### Gestione deployment

- **Logs**: Dashboard Streamlit Cloud → App logs
- **Riavvio**: Dashboard → Reboot app
- **Aggiornamenti**: Ogni push su `main` rideploya automaticamente

---

## ⚙️ Configurazione

### Parametri configurabili

| Parametro | Descrizione | Range | Default |
|-----------|-------------|-------|---------|
| `BASE_URL` | URL pubblico dell'app | String | `https://presenze-aula-unical.streamlit.app/` |
| `ALLOWED_DOMAINS` | Domini consentiti per forms | List | `["forms.office.com", "forms.microsoft.com"]` |
| `DEFAULT_INTERVAL` | Intervallo predefinito (sec) | 30-300 | 60 |
| `MIN_INTERVAL` | Intervallo minimo (sec) | ≥30 | 30 |
| `MAX_INTERVAL` | Intervallo massimo (sec) | ≤300 | 300 |

### Personalizzazione

#### Aggiungere altri domini form

```python
# In app.py, riga 22
ALLOWED_DOMAINS = [
    "forms.office.com",
    "forms.microsoft.com",
    "docs.google.com"  # Aggiungi Google Forms
]
```

#### Modificare intervallo di default

```python
# In app.py, riga 23
DEFAULT_INTERVAL = 90  # 90 secondi invece di 60
```

---

## ❓ FAQ

<details>
<summary><strong>Cosa succede se uno studente scansiona un QR scaduto?</strong></summary>

Il sistema mostra il messaggio: *"⛔ QR scaduto o non valido. Richiedi un nuovo QR al docente."*

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
<summary><strong>Funziona offline?</strong></summary>

No. Serve connessione internet per:
- Generare QR (docente)
- Validare token (app)
- Inviare form (studente)
</details>

---

## 🤝 Contribuire

Contributi, segnalazioni bug e richieste di funzionalità sono benvenuti!

### Come contribuire

1. **Fork** il progetto
2. **Crea** un branch per la feature (`git checkout -b feature/NuovaFunzione`)
3. **Commit** le modifiche (`git commit -m 'Aggiunge NuovaFunzione'`)
4. **Push** al branch (`git push origin feature/NuovaFunzione`)
5. **Apri** una Pull Request

### Segnalare bug

Apri una [Issue](https://github.com/fdr-unical/presenze-aula-unical/issues) descrivendo:
- Comportamento atteso vs comportamento osservato
- Step per riprodurre il bug
- Screenshot (se applicabile)
- Ambiente (OS, browser, versione Python)

---

## 📝 Licenza

Questo progetto è rilasciato sotto licenza **MIT License**.

Vedi il file [LICENSE](LICENSE) per maggiori dettagli.

---

## 🙏 Riconoscimenti

- [Streamlit](https://streamlit.io) - Framework per web app Python
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) - Generazione QR code
- [streamlit-autorefresh](https://github.com/kmcgrady/streamlit-autorefresh) - Componente auto-refresh
- [Microsoft Forms](https://forms.office.com) - Sistema di raccolta dati

---

## 📧 Contatti

Per domande o supporto:
- **Issues**: [https://github.com/fdr-unical/presenze-aula-unical/issues](https://github.com/fdr-unical/presenze-aula-unical/issues)
- **Repository**: [https://github.com/fdr-unical/presenze-aula-unical](https://github.com/fdr-unical/presenze-aula-unical)
- **Università della Calabria**: [www.unical.it](https://www.unical.it)

---

<p align="center">
  Realizzato con ❤️ per <a href="https://www.unical.it">Università della Calabria</a>
</p>
