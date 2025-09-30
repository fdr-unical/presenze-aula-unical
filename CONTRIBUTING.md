# Contribuire a Presenze Aula Unical

Grazie per l'interesse nel contribuire al progetto! 🎉

**Mantenitore**: [Francesco De Rango](mailto:francesco.derango@unical.it)

## Come posso contribuire?

### 🐛 Segnalare bug

Se trovi un bug, apri una [Issue](https://github.com/fdr-unical/presenze-aula-unical/issues) includendo:

1. **Descrizione chiara** del problema
2. **Step per riprodurre** il bug
3. **Comportamento atteso** vs **comportamento osservato**
4. **Screenshot** (se applicabile)
5. **Ambiente**:
   - Sistema operativo
   - Browser e versione
   - Versione Python (se locale)
   - URL app (live o locale)

### 💡 Proporre nuove funzionalità

Hai un'idea per migliorare l'app? Fantastico!

1. Controlla prima le [Issues esistenti](https://github.com/fdr-unical/presenze-aula-unical/issues) per evitare duplicati
2. Apri una nuova Issue con:
   - **Descrizione dettagliata** della funzionalità
   - **Caso d'uso** e benefici
   - **Mockup/sketch** (opzionale ma utile)

### 🔧 Inviare Pull Request

#### Setup ambiente di sviluppo

```bash
# 1. Fork il repository su GitHub

# 2. Clona il tuo fork
git clone https://github.com/fdr-unical/presenze-aula-unical.git
cd presenze-aula-unical

# 3. Crea un branch per la tua feature
git checkout -b feature/nome-funzionalità

# 4. Usa lo script di avvio per setup automatico
# Windows: start.bat
# Linux/macOS: ./start.sh
```

#### Linee guida per il codice

**Stile Python:**
- Usa [Black](https://black.readthedocs.io/) per formattazione: `black app.py`
- Segui [PEP 8](https://peps.python.org/pep-0008/)
- Aggiungi **type hints** dove possibile
- Documenta funzioni con **docstring**

**Commit:**
- Usa messaggi chiari e descrittivi
- Formato: `tipo: descrizione breve`
- Tipi comuni: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

```bash
git commit -m "feat: aggiunge supporto Google Forms"
git commit -m "fix: risolve bug validazione URL"
git commit -m "docs: aggiorna README con esempi"
```

#### Workflow Pull Request

1. **Scrivi il codice** e testa localmente
2. **Formatta** con Black: `black app.py`
3. **Commit** con messaggio descrittivo
4. **Push** al tuo fork: `git push origin feature/nome-funzionalità`
5. **Apri Pull Request** su GitHub
6. **Descrivi** le modifiche nella PR

#### Checklist PR

- [ ] Il codice è formattato con Black
- [ ] Ho testato le modifiche localmente
- [ ] Ho aggiornato la documentazione (README/docstring)
- [ ] Ho aggiunto test (se applicabile)
- [ ] La PR risolve una Issue esistente (linkala nella descrizione)
- [ ] Ho aggiornato CHANGELOG.md con le modifiche

### 📚 Migliorare la documentazione

La documentazione è importante quanto il codice!

- Correggi typo nel README
- Aggiungi esempi d'uso
- Migliora le FAQ
- Traduci in altre lingue
- Aggiungi screenshot/video tutorial

## Domande?

Se hai dubbi, apri una [Discussion](https://github.com/fdr-unical/presenze-aula-unical/discussions) o contatta via email:
📧 [francesco.derango@unical.it](mailto:francesco.derango@unical.it)

## Codice di Condotta

Sii rispettoso e costruttivo. Questo è un progetto open source educativo.

### Comportamenti incoraggiati:
- ✅ Linguaggio rispettoso e inclusivo
- ✅ Critiche costruttive
- ✅ Aiutare altri contributor
- ✅ Condividere conoscenze

### Comportamenti non accettati:
- ⛔ Linguaggio offensivo o discriminatorio
- ⛔ Spam o self-promotion
- ⛔ Trolling o attacchi personali

---

Grazie per contribuire! 🙏

Il tuo contributo aiuta a migliorare l'esperienza educativa di studenti e docenti.

---

**Progetto mantenuto da**: Francesco De Rango ([francesco.derango@unical.it](mailto:francesco.derango@unical.it))
