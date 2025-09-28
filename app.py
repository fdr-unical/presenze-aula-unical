# app.py - Presenze Aula Unical (genera QR che punta al validatore check_token.py)
from datetime import datetime, timezone
import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
import io
import time

st.set_page_config(page_title="Presenze Aula Unical", layout="centered")

st.title("Presenze Aula Unical")
st.caption("Genera un QR code dinamico per registrare le presenze tramite Microsoft Forms.")

st.sidebar.header("Impostazioni")
form_link = st.sidebar.text_input(
    "Link al Microsoft Form",
    help="Incolla qui il link del tuo Form di presenze."
)
interval_s = st.sidebar.number_input(
    "Intervallo rotazione (secondi)",
    min_value=10, max_value=300, value=60, step=10
)

# URL base del validatore (deve essere accessibile agli studenti)
VALIDATOR_URL = "http://localhost:8501/check_token"  # cambia con l'IP o dominio pubblico

def floor_time_to_interval(t: datetime, seconds: int) -> datetime:
    epoch = int(t.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=t.tzinfo)

if form_link:
    now = datetime.now(timezone.utc)
    now_floored = floor_time_to_interval(now, int(interval_s))
    token = now_floored.strftime("%Y%m%d%H%M%S")

    # Costruisco URL con token + form
    target_url = f"{VALIDATOR_URL}?token={token}&form={form_link.strip()}"

    # calcolo countdown
    seconds_passed = int(now.timestamp()) % interval_s
    seconds_left = interval_s - seconds_passed

    # QR code
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(target_url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    st.subheader("QR attuale")
    st.image(buf.getvalue(), caption="Scansiona per registrare la presenza", use_container_width=True)

    st.download_button("Scarica QR", data=buf.getvalue(), file_name="qrcode_presenze.png", mime="image/png")

    st.info(f"Token attuale: {token} · Intervallo: {interval_s}s")
    st.write(f"⏳ Il QR si aggiornerà tra **{seconds_left} secondi**.")

    # refresh ogni secondo per countdown
    time.sleep(1)
    st.rerun()
else:
    st.warning("Incolla nella sidebar il link del tuo Form per generare il QR.")
