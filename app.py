# app.py - Presenze Aula Unical - VERSIONE COMPLETA CORRETTA
# Autore: Francesco De Rango <francesco.derango@unical.it>
# Repository: https://github.com/fdr-unical/presenze-aula-unical
# Licenza: MIT

from datetime import datetime, timezone
import html
import io
from urllib.parse import urlencode, urlparse

import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
import validators
from streamlit_autorefresh import st_autorefresh

# Configurazione pagina
st.set_page_config(
    page_title="Presenze Aula Unical",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Costanti
BASE_URL = "https://presenze-aula-unical.streamlit.app/"
ALLOWED_DOMAINS = ["forms.office.com", "forms.microsoft.com"]
DEFAULT_INTERVAL = 60
MIN_INTERVAL = 30
MAX_INTERVAL = 300

# ---------------------
# Funzioni Utility
# ---------------------

def floor_time_to_interval(t: datetime, seconds: int) -> datetime:
    """Arrotonda un timestamp all'intervallo precedente."""
    epoch = int(t.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=t.tzinfo)


def make_qr_png(url: str) -> bytes:
    """Genera un QR code come immagine PNG."""
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def validate_form_url(url: str) -> bool:
    """Valida che l'URL sia un Microsoft Form legittimo."""
    if not url or not validators.url(url):
        return False

    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in ALLOWED_DOMAINS)


def generate_token(timestamp: datetime, interval: int) -> str:
    """Genera un token temporale univoco."""
    floored = floor_time_to_interval(timestamp, interval)
    return floored.strftime("%Y%m%d%H%M%S")

def validate_token(token: str, interval: int, use_utc: bool) -> bool:
    """Valida un token verificando anche il grace period."""
    if not token:
        return False

    now = datetime.now(timezone.utc if use_utc else None)

    # Token corrente
    current_token = generate_token(now, interval)
    if token == current_token:
        return True

    # Token precedente (grace period)
    prev_time = datetime.fromtimestamp(now.timestamp() - interval, tz=now.tzinfo)
    previous_token = generate_token(prev_time, interval)
    if token == previous_token:
        return True
    
    # CORREZIONE: Token successivo per latenze di rete
    next_time = datetime.fromtimestamp(now.timestamp() + interval, tz=now.tzinfo)
    next_token = generate_token(next_time, interval)
    return token == next_token


def create_qr_url(token: str, form_url: str, interval: int, use_utc: bool) -> str:
    """Crea l'URL completo per il QR code."""
    params = {
        'token': token,
        'to': form_url,
        'interval': interval,
        'utc': 1 if use_utc else 0
    }
    return f"{BASE_URL}?{urlencode(params)}"


# ---------------------
# Modalità Studente
# ---------------------
params = st.query_params

if "token" in params:
    token_qp = params.get("token")
    to_qp = params.get("to")
    interval_s = int(params.get("interval", DEFAULT_INTERVAL))
    use_utc = params.get("utc") == "1"

    # Validazione URL destinazione
    if not validate_form_url(to_qp):
        st.error("⛔ URL non valido o non autorizzato.")
        st.stop()

    # Validazione token
    if validate_token(token_qp, interval_s, use_utc):
        st.success("✅ Token valido. Reindirizzamento in corso…")

        # CORREZIONE: Redirect sicuro IMMEDIATO
        safe_url = html.escape(to_qp, quote=True)
        redirect_html = f"""
        <script>
        window.location.href = "{safe_url}";
        </script>
        <meta http-equiv="refresh" content="0; url={safe_url}">
        <p><strong><a href="{safe_url}" target="_blank">Clicca qui se non vieni reindirizzato</a></strong></p>
        """
        st.components.v1.html(redirect_html, height=100)
        st.stop()
    else:
        st.error("⛔ QR scaduto o non valido. Richiedi un nuovo QR al docente.")
        st.stop()

# ---------------------
# Modalità Docente
# ---------------------

# Inizializza session state
if 'qr_refresh_count' not in st.session_state:
    st.session_state.qr_refresh_count = 0

st.title("🎓 Presenze Aula Unical")
st.caption("Genera un QR dinamico che porta al tuo Microsoft Form, valido solo per pochi secondi.")

# Sidebar configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")

    form_link = st.text_input(
        "Link Microsoft Form",
        placeholder="https://forms.office.com/...",
        help="Incolla qui il link del tuo Microsoft Form"
    )

    # CORREZIONE: Cambiato da 'intervals' a 'interval_s' per consistenza
    interval_s = st.number_input(
        "Intervallo di validità (secondi)",
        min_value=MIN_INTERVAL,
        max_value=MAX_INTERVAL,
        value=DEFAULT_INTERVAL,
        step=30,
        help="Durata di validità del QR code"
    )

    utc_time = st.checkbox(
        "Usa orario UTC",
        value=False,
        help="Usa UTC invece dell'orario locale"
    )
    
    # Debug mode opzionale
    debug_mode = st.checkbox("Debug Mode", value=False)

    if form_link and not validate_form_url(form_link):
        st.error("❌ URL non valido. Inserisci un link Microsoft Forms.")

# Area principale
if form_link and validate_form_url(form_link):
    # Calcola timestamp e token
    now = datetime.now(timezone.utc if utc_time else None)
    token = generate_token(now, interval_s)
    qr_target = create_qr_url(token, form_link, interval_s, utc_time)

    # Genera QR code
    st.subheader("📱 QR Code Attuale")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        png_bytes = make_qr_png(qr_target)
        st.image(png_bytes, use_container_width=True)

    # CORREZIONE PRINCIPALE: Calcola tempo rimanente
    floored = floor_time_to_interval(now, interval_s)
    seconds_since_floored = int((now - floored).total_seconds())
    seconds_left = interval_s - seconds_since_floored

    # CORREZIONE: Auto-refresh continuo senza limite
    count = st_autorefresh(interval=1000, key="qr_timer_continuous")

    # CORREZIONE: Calcolo remaining corretto
    remaining = max(0, seconds_left - (count % interval_s))
    
    # Debug info se abilitato
    if debug_mode:
        st.sidebar.write(f"Now: {now}")
        st.sidebar.write(f"Floored: {floored}")
        st.sidebar.write(f"Seconds since floored: {seconds_since_floored}")
        st.sidebar.write(f"Seconds left: {seconds_left}")
        st.sidebar.write(f"Count: {count}")
        st.sidebar.write(f"Remaining: {remaining}")

    if remaining > 0:
        # Progress bar
        progress = min(1.0, (interval_s - remaining) / interval_s)
        st.progress(progress)

        # Info countdown
        st.info(
            f"⏳ Il QR si aggiornerà automaticamente tra **{remaining}** secondi\n\n"
            f"🔑 Token corrente: `{token}`"
        )
    else:
        # CORREZIONE: Forzare rerun quando necessario
        st.warning("🔄 Aggiornamento QR in corso...")
        st.session_state.qr_refresh_count += 1
        st.rerun()

    # Istruzioni per studenti
    with st.expander("📋 Istruzioni per gli studenti"):
        st.markdown(f"""
        1. **Scansiona** il QR code con la fotocamera del tuo smartphone
        2. **Verrai reindirizzato** automaticamente al form di presenza
        3. **Compila** il form entro il tempo indicato

        ⚠️ **Importante**: Il QR code cambia ogni {interval_s} secondi per motivi di sicurezza.
        """)

    # Informazioni tecniche
    with st.expander("🔧 Dettagli tecnici"):
        st.markdown(f"""
        - **Intervallo**: {interval_s} secondi
        - **Timezone**: {"UTC" if utc_time else "Locale"}
        - **URL Form**: `{form_link[:50]}...`
        - **Grace Period**: Sì (token precedente e successivo accettati)
        """)

else:
    # Schermata iniziale
    st.info("👈 Inserisci il link del tuo Microsoft Form nella barra laterale per iniziare.")

    st.markdown("""
    ### Come funziona?

    1. **Docente**: Inserisci il link del Microsoft Form nella sidebar
    2. **Sistema**: Genera un QR code dinamico che cambia automaticamente
    3. **Studente**: Scansiona il QR per registrare la presenza
    4. **Sicurezza**: Ogni QR è valido solo per pochi secondi

    ### Vantaggi

    ✅ **Sicuro**: QR code temporizzati impediscono condivisioni fraudolente  
    ✅ **Semplice**: Nessuna registrazione o login richiesta  
    ✅ **Automatico**: Il QR si aggiorna da solo in tempo reale  
    ✅ **Affidabile**: Grace period per problemi di sincronizzazione  
    """)

# Footer con info versione
st.markdown("---")
st.caption(f"🔧 App version 2.1 - Fixed | Remaining: {remaining if 'remaining' in locals() else 'N/A'}s")
