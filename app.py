# app.py - Presenze Aula Unical (unica app Streamlit con generazione QR e validazione token)
from datetime import datetime, timezone
import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
import io
import time

st.set_page_config(page_title="Presenze Aula Unical", layout="centered")

st.title("Presenze Aula Unical")
st.caption("QR code dinamico con validazione automatica del token per Microsoft Forms.")

# --- Sidebar docente ---
st.sidebar.header("Configurazione docente")
form_link = st.sidebar.text_input("Link al Microsoft Form", help="Incolla qui il link del tuo Form")
interval_s = st.sidebar.number_input("Intervallo rotazione (secondi)", 10, 300, 60, 10)

# --- Funzione supporto ---
def floor_time_to_interval(t: datetime, seconds: int) -> datetime:
    epoch = int(t.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=t.tzinfo)

# --- Modalità docente: genera QR ---
if "mode" not in st.query_params:
    if not form_link:
        st.warning("Inserisci il link del Microsoft Form nella sidebar per iniziare.")
    else:
        now = datetime.now(timezone.utc)
        now_floored = floor_time_to_interval(now, int(interval_s))
        token = now_floored.strftime("%Y%m%d%H%M%S")

        # URL verso la stessa app, in modalità 'check'
        target_url = f"{st.request.host_url}?mode=check&token={token}"

        # Countdown
        seconds_passed = int(now.timestamp()) % interval_s
        seconds_left = interval_s - seconds_passed

        # Genera QR code
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(target_url)
        qr.make(fit=True)
        img: PilImage = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")

        st.subheader("QR attuale")
        st.image(buf.getvalue(), caption="Scansiona per registrare la presenza", use_container_width=True)

        st.download_button("Scarica QR", data=buf.getvalue(),
                           file_name="qrcode_presenze.png", mime="image/png")

        st.info(f"Token attuale: {token} · Intervallo: {interval_s}s")
        st.write(f"⏳ Il QR si aggiornerà tra **{seconds_left} secondi**.")

        # Refresh ogni secondo per aggiornare countdown
        time.sleep(1)
        st.rerun()

# --- Modalità studente: controllo token ---
else:
    params = st.query_params
    token = params.get("token", [""])[0] if "token" in params else None

    if not form_link:
        st.error("Il docente non ha ancora configurato il link del modulo.")
    elif not token:
        st.error("Nessun codice valido nel QR.")
    else:
        try:
            token_time = datetime.strptime(token, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = (now - token_time).total_seconds()

            if 0 <= diff < interval_s:
                st.success("Codice valido! Verrai reindirizzato al modulo.")
                st.markdown(f"[Apri il modulo qui]({form_link})", unsafe_allow_html=True)

                # Redirect automatico
                st.markdown(
                    f'<meta http-equiv="refresh" content="0;url={form_link}">',
                    unsafe_allow_html=True
                )
            else:
                st.error(" Questo QR code è scaduto. Richiedi al docente quello aggiornato.")
        except Exception:
            st.error("Codice non valido.")
