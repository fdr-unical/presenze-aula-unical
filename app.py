import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import time
import validators
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timezone
import math

# ============================================================
# CONFIGURAZIONE
# ============================================================
BASE_URL = "https://presenze-aula-unical.streamlit.app/"
ALLOWED_DOMAINS = ["forms.office.com", "forms.microsoft.com"]
DEFAULT_INTERVAL = 60  # secondi
MIN_INTERVAL = 30
MAX_INTERVAL = 300

# ============================================================
# FUNZIONI UTILITÀ
# ============================================================

def validate_form_url(url):
    """Valida l'URL del form Microsoft"""
    if not validators.url(url):
        return False, "URL non valido"

    for domain in ALLOWED_DOMAINS:
        if domain in url:
            return True, "URL valido"

    return False, f"URL deve contenere uno di: {', '.join(ALLOWED_DOMAINS)}"

def generate_token(interval_seconds=60):
    """Genera token basato sul tempo corrente"""
    now_utc = datetime.now(timezone.utc)
    timestamp = int(now_utc.timestamp())
    bin_number = math.floor(timestamp / interval_seconds)
    return bin_number

def is_token_valid(token, interval_seconds=60, grace_period=True):
    """Verifica se un token è ancora valido"""
    current_token = generate_token(interval_seconds)

    if token == current_token:
        return True

    # Grace period: accetta anche il token dell'intervallo precedente
    if grace_period and token == (current_token - 1):
        return True

    return False

def generate_qr_url(form_url, token):
    """Genera URL con token per validazione"""
    return f"{BASE_URL}?token={token}&redirect={form_url}"

def generate_qr_code(url, size=300):
    """Genera QR code come immagine PIL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))
    return img

def get_time_remaining(interval_seconds=60):
    """Calcola secondi rimanenti nell'intervallo corrente"""
    now_utc = datetime.now(timezone.utc)
    timestamp = int(now_utc.timestamp())
    seconds_in_interval = timestamp % interval_seconds
    return interval_seconds - seconds_in_interval

# ============================================================
# CONFIGURAZIONE PAGINA
# ============================================================

st.set_page_config(
    page_title="QR Code Presenze - UnICal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# GESTIONE URL PARAMETERS (Validazione Token)
# ============================================================

query_params = st.query_params

if "token" in query_params and "redirect" in query_params:
    # Modalità validazione studente
    try:
        token = int(query_params["token"])
        redirect_url = query_params["redirect"]
        interval = int(query_params.get("interval", DEFAULT_INTERVAL))

        if is_token_valid(token, interval):
            st.success("✅ Token valido! Reindirizzamento al form...")
            st.markdown(f"""
            <meta http-equiv="refresh" content="0;url={redirect_url}">
            <script>window.location.href = '{redirect_url}';</script>
            """, unsafe_allow_html=True)
            st.markdown(f"[Se non vieni reindirizzato automaticamente, clicca qui]({redirect_url})")
            st.stop()
        else:
            st.error("⛔ QR Code scaduto o non valido")
            st.warning("Richiedi un nuovo QR code al docente.")
            st.stop()

    except ValueError:
        st.error("❌ Token non valido")
        st.stop()

# ============================================================
# MODALITÀ DOCENTE - GENERAZIONE QR CODE
# ============================================================

st.title("🎓 QR Code Presenze Aula")
st.markdown("**Università della Calabria** - Sistema anti-frode con token temporizzati")

# Sidebar - Configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")

    form_url = st.text_input(
        "URL Form Microsoft",
        placeholder="https://forms.office.com/...",
        help="Inserisci l'URL completo del tuo Microsoft Form"
    )

    interval = st.slider(
        "Intervallo aggiornamento (secondi)",
        min_value=MIN_INTERVAL,
        max_value=MAX_INTERVAL,
        value=DEFAULT_INTERVAL,
        step=10,
        help="Frequenza di rotazione del QR code"
    )

    qr_size = st.slider(
        "Dimensione QR Code",
        min_value=200,
        max_value=500,
        value=300,
        step=50
    )

    st.markdown("---")
    st.markdown("### 📖 Come funziona")
    st.markdown("""
    1. Inserisci l'URL del form Microsoft
    2. Il QR code si aggiorna ogni {} secondi
    3. Gli studenti scansionano il QR code
    4. Il sistema valida il token server-side
    5. Se valido, redirect al form
    """.format(interval))

    st.markdown("---")
    st.markdown("**Autore**: Francesco De Rango  
**UnICal** - 2025")

# Validazione URL
if form_url:
    is_valid, message = validate_form_url(form_url)

    if not is_valid:
        st.error(f"❌ {message}")
        st.stop()

    st.success(f"✅ {message}")

    # Genera token corrente
    current_token = generate_token(interval)
    qr_url = generate_qr_url(form_url, current_token)
    qr_url_with_interval = f"{qr_url}&interval={interval}"

    # Genera QR code
    qr_img = generate_qr_code(qr_url_with_interval, qr_size)

    # Layout a colonne
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image(qr_img, caption="Scansiona questo QR code", use_container_width=True)

    with col2:
        time_remaining = get_time_remaining(interval)

        st.metric("⏱️ Tempo rimanente", f"{time_remaining}s")
        st.metric("🔢 Token corrente", current_token)

        # Progress bar
        progress = (interval - time_remaining) / interval
        st.progress(progress)

        st.info(f"🔄 Prossimo aggiornamento tra {time_remaining} secondi")

    # Info aggiuntive
    st.markdown("---")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("📅 Data", datetime.now().strftime("%d/%m/%Y"))

    with col_b:
        st.metric("🕐 Ora", datetime.now().strftime("%H:%M:%S"))

    with col_c:
        st.metric("⏰ Intervallo", f"{interval}s")

    # Download QR code
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    st.download_button(
        label="📥 Scarica QR Code",
        data=buf,
        file_name=f"qr_presenze_{current_token}.png",
        mime="image/png"
    )

    # Auto-refresh per aggiornare il QR code
    st_autorefresh(interval=time_remaining * 1000, key="qr_refresh")

else:
    st.info("👈 Inserisci l'URL del form Microsoft nella sidebar per generare il QR code")

    st.markdown("### 🔒 Caratteristiche di sicurezza")
    st.markdown("""
    - **Token temporizzati**: Ogni QR code è valido solo per un intervallo di tempo configurabile
    - **Validazione server-side**: Il token viene verificato dal server prima del redirect
    - **Grace period**: Token dell'intervallo precedente accettati per sincronizzazione
    - **Whitelist domini**: Solo URL Microsoft Forms accettati
    - **Anti-condivisione**: Screenshot/link condivisi diventano invalidi rapidamente
    """)

    st.markdown("### 🎯 Caso d'uso")
    st.markdown("""
    Sistema sviluppato per classi di 200+ studenti presso l'Università della Calabria.
    Il QR code dinamico impedisce agli studenti di condividere il link con colleghi assenti.
    """)
