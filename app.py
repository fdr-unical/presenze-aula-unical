# app.py — Presenze Aula Unical (QR dinamico + verifica token, URL intermedio automatico)
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import html
import time

import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
import io


st.set_page_config(page_title="Presenze Aula Unical", layout="centered")


def floor_time_to_interval(t: datetime, seconds: int) -> datetime:
    epoch = int(t.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=t.tzinfo)

def safe_get_query_param(name: str, default=None):
    try:
        return st.query_params.get(name, default)
    except Exception:
        qp = st.experimental_get_query_params()
        return qp.get(name, [default])[0]

def build_url(base_url: str, extra_params: dict) -> str:
    parts = urlparse(base_url)
    qs = dict(parse_qsl(parts.query, keep_blank_values=True))
    qs.update({k: str(v) for k, v in extra_params.items() if v is not None})
    new_query = urlencode(qs)
    path = parts.path or "/"
    return urlunparse((parts.scheme, parts.netloc, path, parts.params, new_query, parts.fragment))

def make_qr_png(data_url: str) -> bytes:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(data_url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def get_base_url() -> str:
    try:
        return st.request.base_url.rstrip("/")
    except Exception:
        return "http://localhost:8501"


# Branch 1: modalità guardiano
token_qp = safe_get_query_param("token")
if token_qp:
    to_qp = safe_get_query_param("to")
    interval_qp = safe_get_query_param("interval")
    utc_qp = safe_get_query_param("utc")
    grace_qp = safe_get_query_param("grace")

    try:
        interval_s = int(interval_qp) if interval_qp else 60
    except Exception:
        interval_s = 60

    use_utc = (utc_qp == "1")
    allow_prev = (grace_qp == "1")

    now = datetime.now(timezone.utc if use_utc else None)

    valid_now = floor_time_to_interval(now, interval_s).strftime("%Y%m%d%H%M%S")
    is_valid = (token_qp == valid_now)

    if not is_valid and allow_prev:
        prev = datetime.fromtimestamp(now.timestamp() - interval_s, tz=now.tzinfo)
        valid_prev = floor_time_to_interval(prev, interval_s).strftime("%Y%m%d%H%M%S")
        is_valid = (token_qp == valid_prev)

    st.title("Verifica accesso")
    if is_valid and to_qp:
        st.success("✅ Token valido. Ti sto reindirizzando al modulo…")
        target = to_qp
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={html.escape(target)}">',
            unsafe_allow_html=True
        )
        st.markdown(f"[Apri il modulo se non vieni reindirizzato automaticamente]({target})")
    else:
        st.error("⛔ Questo QR è scaduto o non valido. Richiedi al docente un nuovo QR.")
    st.stop()


# Branch 2: modalità docente
st.title("Presenze Aula Unical")
st.caption("Genera un QR code dinamico con token a scadenza e verifica lato server (in questa stessa app).")

st.sidebar.header("Impostazioni")
form_link = st.sidebar.text_input("Link al Microsoft Form", help="Incolla il link del tuo Form di presenze.")
interval_s = st.sidebar.number_input("Intervallo rotazione (secondi)", min_value=10, max_value=300, value=60, step=10)
utc_time = st.sidebar.checkbox("Usa orario UTC", value=False)
grace_prev = st.sidebar.checkbox("Tolleranza: accetta anche l’intervallo precedente (consigliato)", value=True)

intermediate_url = get_base_url()
st.sidebar.info(f"URL intermedio usato automaticamente: {intermediate_url}")

if form_link:
    now = datetime.now(timezone.utc if utc_time else None)
    now_floored = floor_time_to_interval(now, int(interval_s))
    token = now_floored.strftime("%Y%m%d%H%M%S")

    qr_target = build_url(
        intermediate_url.strip(),
        {
            "token": token,
            "to": form_link.strip(),
            "interval": int(interval_s),
            "utc": 1 if utc_time else 0,
            "grace": 1 if grace_prev else 0
        }
    )

    st.subheader("QR attuale")
    png_bytes = make_qr_png(qr_target)
    st.image(png_bytes, caption="Scansiona per registrare la presenza", use_container_width=True)
    st.download_button("Scarica QR", data=png_bytes, file_name="qrcode_presenze.png", mime="image/png")

    seconds_passed = int(now.timestamp()) % int(interval_s)
    seconds_left = int(interval_s) - seconds_passed
    st.info(f"Token attuale: {token} · Intervallo: {interval_s}s · URL intermedio: {intermediate_url}")

    progress_bar = st.progress(0, text=f"⏳ Il QR si aggiornerà tra {seconds_left} secondi")
    for i in range(seconds_left, 0, -1):
        progress_bar.progress((seconds_left - i + 1) / max(seconds_left, 1),
                              text=f"⏳ Il QR si aggiornerà tra {i} secondi")
        time.sleep(1)

    st.rerun()
else:
    st.warning("Incolla nella sidebar il link del tuo Form per generare il QR.")
