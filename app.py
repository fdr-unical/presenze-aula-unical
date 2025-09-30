# app.py - Presenze Aula Unical
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

def validate_token(token: str, interval: int, use_utc: bool) 
