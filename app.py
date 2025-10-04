import streamlit as st
import time
import hashlib
from datetime import datetime
import pandas as pd

# Configurazione pagina
st.set_page_config(
    page_title="Presenze Aula - UniCal",
    page_icon="📋",
    layout="wide"
)

# CSS personalizzato
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 2px solid #28a745;
        margin: 20px 0;
    }
    .error-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        margin: 20px 0;
    }
    .warning-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Funzione per generare token
def generate_token(period=60):
    """Genera token basato su timestamp corrente"""
    now_sec = int(time.time())
    bin_value = now_sec // period
    return str(bin_value)

# Funzione per validare token
def validate_token(token, period=60, tolerance=0):
    """
    Valida se il token è ancora valido
    tolerance: numero di periodi precedenti da accettare (0 = solo corrente)
    """
    current_token = generate_token(period)

    # Controlla token corrente
    if token == current_token:
        return True, "Token valido (periodo corrente)"

    # Controlla periodi precedenti se tolerance > 0
    if tolerance > 0:
        for i in range(1, tolerance + 1):
            now_sec = int(time.time())
            previous_bin = (now_sec // period) - i
            if token == str(previous_bin):
                return True, f"Token valido (periodo precedente -{i})"

    return False, "Token scaduto o non valido"

# Funzione per salvare presenza
def save_attendance(student_name, student_id, token, period):
    """Salva presenza nel database (simulato)"""
    timestamp = datetime.now()
    is_valid, message = validate_token(token, period, tolerance=1)

    if is_valid:
        # In produzione: salvare in database
        attendance_record = {
            "timestamp": timestamp,
            "student_name": student_name,
            "student_id": student_id,
            "token": token,
            "status": "presente",
            "message": message
        }
        return True, attendance_record
    else:
        return False, {"message": message}

# Titolo principale
st.title("📋 Sistema Presenze Aula - UniCal")
st.markdown("### Rilevazione Presenze con QR Code Dinamico")

# Sidebar configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")

    # Modalità
    mode = st.radio(
        "Modalità:",
        ["Studente (Registra Presenza)", "Docente (Genera QR Code)"],
        index=0
    )

    st.divider()

    # Impostazioni avanzate
    with st.expander("🔧 Impostazioni Avanzate"):
        period = st.slider(
            "Intervallo QR Code (secondi)",
            min_value=45,
            max_value=180,
            value=60,
            step=15,
            help="Tempo di validità di ogni QR code"
        )

        tolerance = st.slider(
            "Tolleranza periodi",
            min_value=0,
            max_value=2,
            value=1,
            help="Accetta token dei periodi precedenti (0=solo corrente, 1=+60s, 2=+120s)"
        )

# ============================================
# MODALITÀ STUDENTE
# ============================================
if mode == "Studente (Registra Presenza)":
    st.markdown("---")
    st.markdown("### 👨‍🎓 Registrazione Presenza Studente")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info("📱 Scansiona il QR code mostrato dal docente e inserisci il token visualizzato.")

        # Form studente
        with st.form("student_form"):
            nome = st.text_input("Nome e Cognome *", placeholder="Mario Rossi")
            matricola = st.text_input("Matricola *", placeholder="123456")
            token_input = st.text_input(
                "Token dal QR Code *", 
                placeholder="Inserisci il numero dal QR code",
                help="Il token è un numero che cambia ogni minuto"
            )

            submitted = st.form_submit_button("✅ Registra Presenza", use_container_width=True)

            if submitted:
                if not nome or not matricola or not token_input:
                    st.error("⚠️ Compila tutti i campi obbligatori")
                else:
                    # Valida e salva presenza
                    success, result = save_attendance(nome, matricola, token_input, period)

                    if success:
                        st.markdown("""
                        <div class="success-box">
                            <h3 style="color: #28a745; margin: 0;">✅ Presenza Registrata!</h3>
                            <p style="margin: 10px 0 0 0;">La tua presenza è stata confermata con successo.</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Mostra dettagli
                        st.success(f"**Nome**: {result['student_name']}")
                        st.success(f"**Matricola**: {result['student_id']}")
                        st.success(f"**Orario**: {result['timestamp'].strftime('%H:%M:%S')}")
                        st.info(f"ℹ️ {result['message']}")
                    else:
                        st.markdown("""
                        <div class="error-box">
                            <h3 style="color: #dc3545; margin: 0;">❌ Errore Registrazione</h3>
                            <p style="margin: 10px 0 0 0;">Il token inserito non è valido o è scaduto.</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.error(f"**Motivo**: {result['message']}")
                        st.warning("💡 **Suggerimento**: Scansiona di nuovo il QR code e riprova immediatamente.")

    with col2:
        st.markdown("#### ℹ️ Informazioni")
        st.markdown("""
        **Come funziona**:
        1. Scansiona il QR code proiettato
        2. Copia il token (numero)
        3. Inserisci i tuoi dati
        4. Click "Registra Presenza"

        **Importante**:
        - Il token cambia ogni minuto
        - Registra subito dopo scansione
        - Usa la tua matricola vera
        """)

        # Mostra token corrente (solo per testing)
        if st.checkbox("🔍 Mostra token corrente (debug)"):
            current_token = generate_token(period)
            st.code(current_token, language="text")
            st.caption(f"Valido per {period} secondi")

# ============================================
# MODALITÀ DOCENTE
# ============================================
else:
    st.markdown("---")
    st.markdown("### 👨‍🏫 Generazione QR Code Docente")

    col1, col2 = st.columns([3, 2])

    with col1:
        # Configurazione
        st.markdown("#### ⚙️ Configurazione Lezione")

        corso = st.text_input("Nome Corso", value="Reti di Calcolatori", placeholder="Es: Algoritmi e Strutture Dati")
        aula = st.text_input("Aula", value="Aula Magna", placeholder="Es: Aula 1B - Cubo 31C")

        if st.button("🚀 Avvia Sistema Presenze", use_container_width=True):
            st.session_state['qr_active'] = True
            st.session_state['start_time'] = datetime.now()

        if st.button("⏹️ Ferma Sistema", use_container_width=True):
            st.session_state['qr_active'] = False

    with col2:
        st.markdown("#### 📊 Statistiche")
        if 'start_time' in st.session_state:
            elapsed = (datetime.now() - st.session_state['start_time']).seconds
            st.metric("⏱️ Tempo attivo", f"{elapsed // 60} min {elapsed % 60} sec")
        st.metric("👥 Presenze registrate", "0")  # In produzione: query database
        st.metric("🔄 Cicli completati", "0")

    # Mostra QR Code se attivo
    if st.session_state.get('qr_active', False):
        st.markdown("---")
        st.markdown("### 📱 QR Code Attivo")

        # Genera token corrente
        current_token = generate_token(period)

        # QR Code URL (in produzione: URL vera del form)
        qr_url = f"https://presenze-aula-unical.streamlit.app/?token={current_token}"

        # Genera QR code usando API
        qr_code_url = f"https://quickchart.io/qr?text={qr_url}&size=400&dark=2c3e50&light=ffffff"

        # Layout QR code
        col_qr1, col_qr2, col_qr3 = st.columns([1, 2, 1])

        with col_qr2:
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background-color: #f8f9fa; border-radius: 15px; border: 3px solid #3498db;">
                <h2 style="color: #2c3e50; margin-bottom: 20px;">Scansiona Questo Codice</h2>
                <img src="{qr_code_url}" style="max-width: 100%; border-radius: 10px;"/>
                <h1 style="color: #3498db; margin-top: 20px; font-family: monospace;">TOKEN: {current_token}</h1>
                <p style="color: #7f8c8d; font-size: 18px; margin-top: 10px;">Valido per {period} secondi</p>
            </div>
            """, unsafe_allow_html=True)

        # Countdown
        st.markdown("---")
        countdown_placeholder = st.empty()

        # Calcola secondi rimanenti
        now_sec = int(time.time())
        elapsed_in_period = now_sec % period
        remaining = period - elapsed_in_period

        # Progress bar
        progress = elapsed_in_period / period
        st.progress(progress)

        # Countdown text
        if remaining > 10:
            countdown_placeholder.success(f"⏱️ **Tempo rimanente**: {remaining} secondi")
        else:
            countdown_placeholder.error(f"⚠️ **Attenzione! Il codice scade tra**: {remaining} secondi")

        # Auto-refresh ogni 5 secondi
        time.sleep(5)
        st.rerun()

    else:
        st.info("👆 Clicca 'Avvia Sistema Presenze' per generare il QR code")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p><strong>Sistema Presenze Aula - Università della Calabria</strong></p>
    <p>Sviluppato con ❤️ da Francesco De Rango</p>
    <p>📧 <a href="mailto:francesco.derango@unical.it">francesco.derango@unical.it</a> | 
    🔗 <a href="https://github.com/fdr-unical">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
