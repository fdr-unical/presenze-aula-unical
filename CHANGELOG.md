# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato si basa su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-30

### ✨ Aggiunto
- Auto-refresh intelligente con `streamlit-autorefresh` (elimina loop sleep bloccanti)
- Progress bar visuale per countdown QR
- Validazione URL con whitelist Microsoft Forms
- Grace period per token (accetta anche token precedente)
- Session state per gestione refresh ottimizzata
- Redirect sicuro con doppio fallback (meta refresh + JavaScript)
- Expander per istruzioni studenti e dettagli tecnici
- Layout responsive con colonne
- Supporto emoji per migliore UX
- Script di avvio automatico (start.bat per Windows, start.sh per Linux/macOS)
- QUICKSTART.md per avvio rapido
- CONTRIBUTING.md per linee guida contributi
- README esteso con 3 modalità d'uso (app live, deploy proprio, sviluppo locale)

### 🔒 Sicurezza
- Validazione URL con libreria `validators`
- Whitelist domini Microsoft Forms
- HTML/JavaScript sanitization per redirect
- Controllo token server-side con grace period
- Error handling robusto

### 🐛 Corretto
- Loop infinito con `time.sleep()` e `st.rerun()`
- Consumo risorse eccessivo del server
- Mancata validazione URL di destinazione
- Gestione query params mancanti
- Meta refresh non funzionante in alcuni browser

### 🔄 Modificato
- Ristrutturazione completa del codice in funzioni modulari
- Miglioramento UI/UX con sidebar strutturata
- Documentazione inline completa
- README esteso con esempi, diagrammi e FAQ
- Script di avvio con gestione errori avanzata

### 🗑️ Rimosso
- Loop `while` con `sleep(1)` (sostituito da auto-refresh)
- Code duplicato per validazione token

---

## [1.0.0] - 2025-XX-XX

### ✨ Aggiunto
- Versione iniziale
- Generazione QR code dinamici
- Validazione token temporizzati
- Supporto Microsoft Forms
- Deploy su Streamlit Cloud

---

## Legenda

- `✨ Aggiunto` per nuove funzionalità
- `🔄 Modificato` per modifiche a funzionalità esistenti
- `🗑️ Rimosso` per funzionalità rimosse
- `🐛 Corretto` per correzioni di bug
- `🔒 Sicurezza` per vulnerabilità risolte
