# Presenze Aula Unical

Questa è una mini-app sviluppata in **Streamlit** per generare **QR code dinamici** (rotativi) da collegare a un **Microsoft Form**.  
L’obiettivo è facilitare la **registrazione delle presenze in aula** in modo sicuro, evitando il riutilizzo di QR statici.

## Funzionalità
- Generazione di QR code che cambia ogni intervallo di tempo (default: 60 secondi).
- Aggiunta di un token temporale all’URL del Form (`?token=YYYYMMDDhhmmss`).
- Download del QR code in formato PNG.
- Interfaccia semplice e pronta per l’uso in aula (proiezione su schermo).

## Flusso
1. Il docente crea un Microsoft Form con i campi: Nome, Cognome, Matricola.
2. Copia il link del Form e lo incolla nell’app.
3. L’app genera un QR code rotativo con token.
4. Gli studenti scansionano il QR e compilano il Form.
5. Le risposte finiscono direttamente nell’account del docente, insieme al token.

## Installazione locale
1. Clona il repository:
   ```bash
   git clone https://github.com/francescoderango/presenze-aula-unical.git
   cd presenze-aula-unical
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Avvia l’app:
   ```bash
   streamlit run app.py
   ```

## Deploy su Streamlit Cloud
Questo progetto è configurato per il deploy diretto su **Streamlit Cloud**.  
Dopo aver collegato il repository, l’app sarà disponibile online con un link del tipo:

```
https://presenze-aula-unical.streamlit.app
```

## Demo
Esempio di tabella esportata da Microsoft Forms con token:

| Nome e Cognome | Matricola | Corso    | Ora di invio        | Token           |
|----------------|-----------|----------|---------------------|-----------------|
| Mario Rossi    | 123456    | Biologia | 28/09/2025 18:45    | 20250928184500 |
| Anna Bianchi   | 654321    | Biologia | 28/09/2025 18:46    | 20250928184600 |

---

© 2025 — Francesco De Rango. Rilasciato con licenza MIT.
