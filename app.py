# app.py - Presenze Aula Unical (versione con grace attivo)
from datetime import datetime, timezone
import time
import html
import io
from urllib.parse import urlencode

import streamlit as st
import qrcode
from qrcode.image.pil import PilImage


st.set_page_config(page_title="Presenze Aula Unical", layout="centered")

def floor_time_to_interval(t: datetime, seconds: int) -> datetime:
    epoch = int(t.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=t.tzinfo)

def make_qr_png(url: str) -> bytes:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

params = st.query_params
if "token" in params:
    token_qp = params.get("token")
    to_qp = params.get("to")

    interval_s = int(params.get("interval", 60))
    use_utc = params.get("utc") == "1"

    now = datetime.now(timezone.utc if use_utc else None)
    valid_now = floor_time_to_interval(now, interval_s).strftime("%Y%m%d%H%M%S")

    # Verifica token attuale o precedente (grace attivo)
    is_valid = (token_qp == valid_now)
    if not is_valid:
        prev = datetime.fromtimestamp(now.timestamp() - interval_s, tz=now.tzinfo)
        valid_prev = floor_time_to_interval(prev, interval_s).strftime("%Y%m%d%H%M%S")
        is_valid = (token_qp == valid_prev)

    if is_valid and to_qp:
        st.success("✅ Token valido. Reindirizzamento in corso…")
        st.markdown(f'<meta http-equiv="refresh" content="0; url={html.escape(to_qp)}">', unsafe_allow_html=True)
        st.stop()
    else:
        st.error("⛔ QR scaduto o non valido. Richiedi un nuovo QR.")
        st.stop()

st.title("Presenze Aula Unical")
st.caption("Genera un QR dinamico che porta al tuo Microsoft Form, valido solo per pochi secondi.")

form_link = st.sidebar.text_input("Link al Microsoft Form")
interval_s = st.sidebar.number_input("Intervallo (secondi)", min_value=30, max_value=300, value=60, step=30)
utc_time = st.sidebar.checkbox("Usa orario UTC", value=False)

# URL pubblico fisso della tua app su Streamlit Cloud
base_url = "https://presenze-aula-unical.streamlit.app/"

if form_link:
    now = datetime.now(timezone.utc if utc_time else None)
    now_floored = floor_time_to_interval(now, interval_s)
    token = now_floored.strftime("%Y%m%d%H%M%S")

    qr_target = f"{base_url}?{urlencode({'token': token, 'to': form_link, 'interval': interval_s, 'utc': 1 if utc_time else 0})}"

    st.subheader("QR attuale")
    png_bytes = make_qr_png(qr_target)
    st.image(png_bytes, caption="Scansiona per registrare la presenza", use_container_width=True)

    seconds_passed = int(now.timestamp()) % interval_s
    seconds_left = interval_s - seconds_passed
    progress = st.progress(0, text=f"⏳ QR si aggiornerà tra {seconds_left} secondi")

    for i in range(seconds_left, 0, -1):
        progress.progress((seconds_left - i + 1) / seconds_left, text=f"⏳ QR si aggiornerà tra {i} secondi")
        time.sleep(1)

    st.rerun()
else:
    st.info("Incolla nella sidebar il link del tuo Microsoft Form per generare il QR.")
