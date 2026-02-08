import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import random
from datetime import datetime

# ==========================================
# ⚙️ 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Quantum Future Path", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #E0E0E0 !important; }
    [data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    .stTextInput > div > div > input { color: white !important; background-color: #0D1117 !important; border: 1px solid #30363D; }
    .stSelectbox > div > div > div { color: white !important; background-color: #0D1117 !important; }
    .stTextArea > div > div > textarea { color: white !important; background-color: #0D1117 !important; }
    div.stButton > button { background-color: #238636 !important; color: white !important; border: none; border-radius: 6px; width: 100%; padding: 0.5rem; }
    div.stButton > button:hover { background-color: #2EA043 !important; }
    h1, h2, h3 { color: #E6EDF3 !important; }
    div[data-testid="stChatMessage"] { background-color: #161B22 !important; border: 1px solid #30363D; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔐 2. SISTEMA DE LOGIN QUANTUM (MODO CINE 🎬)
# ==========================================
if "usuario_activo" not in st.session_state:
    # --- CSS ESPECÍFICO PARA EL LOGIN (FONDO PANTALLA COMPLETA) ---
    st.markdown(f"""
        <style>
        /* 1. Ocultar la Sidebar y la barra superior solo en el Login */
        [data-testid="stSidebar"] {{ display: none; }}
        [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); }}
        
        /* 2. Imagen de Fondo que cubre TODO */
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        /* 3. Tarjeta Central (Efecto Cristal) */
        .login-card {{
            background-color: rgba(14, 22, 33, 0.85); /* Fondo oscuro semitransparente */
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #30363D;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 400px;
            margin: 0 auto;
            margin-top: 100px; /* Bajarla un poco */
        }}
        h2 {{ color: white !important; }}
        p {{ color: #b0b8c4 !important; }}
        </style>
        """, unsafe_allow_html=True)

    # --- ESTRUCTURA VISUAL ---
    # Usamos columnas para centrar la "Tarjeta"
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Creamos el contenedor visual con HTML
        st.markdown("""
        <div class="login-card">
            <h2 style='margin-bottom: 10px;'>Quantum Future Path 🚀</h2>
            <p style='margin-bottom: 20px;'>Diseña tu futuro a prueba de obsolescencia.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inputs de Streamlit (fuera del HTML para que funcionen)
        # Usamos un contenedor vacío para estilizar un poco mejor la posición
        st.markdown("<div style='max-width: 400px; margin: 0 auto;'>", unsafe_allow_html=True)
        clave_input = st.text_input("Ingresa tu Clave de Acceso:", type="password", placeholder="DEMO", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 INICIAR VIAJE", use_container_width=True):
            llaves_validas = st.secrets.get("access_keys", {})
            if clave_input in llaves_validas:
                st.session_state.usuario_activo = llaves_validas[clave_input]
                st.rerun()
            else:
                st.error("⛔ Clave incorrecta. Intenta con DEMO.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop() # 🛑 DETIENE TODO AQUÍ SI NO ESTÁ LOGUEADO

# ==========================================
# 🧠 3. CONEXIÓN CON GEMINI
# ==========================================
model = None 
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Error conectando con Gemini: {e}")
else:
    st.warning("⚠️ Falta configurar la GOOGLE_API_KEY en los Secrets.")

# ==========================================
# 🛠️ 4. FUNCIONES
# ==========================================
def limpiar_texto(texto):
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def generar_pdf_blindado(nombre, perfil, analisis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(22, 27, 34)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, txt="Quantum Future Path", ln=1, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, txt="Plan de Carrera Blindado contra Obsolescencia", ln=1, align='C')
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=limpiar_texto(f"Estudiante: {nombre}"), ln=1)
    pdf.cell(0, 10, txt=limpiar_texto(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}"), ln=1)
    pdf.ln(5)
    pdf.set_font("Arial", '', 11)
    for linea in analisis.split('\n'):
        linea_limpia = linea.replace('**', '').replace('*', '-')
        pdf.multi_cell(0, 7, txt=limpiar_texto(linea_limpia))
        pdf.ln(1)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 🏠 5. INTERFAZ (SIDEBAR) - Solo visible tras Login
# ==========================================
with st.sidebar:
    try: st.image("logo_quantum.png", use_container_width=True)
    except: st.header("Quantum 🚀")
    
    st.caption(f"Sesión: **{st.session_state.usuario_activo}**") # Muestra quién está conectado
    
    st.title("Parámetros de Diseño")
    if "visitas" not in st.session_state: st.session_state.visitas = random.randint(1200, 1800)
    st.metric("👀 Estudiantes Orientados", f"{st.session_state.visitas:,}")
    st.markdown("---")
    
    nombre = st.text_input("Nombre:", "Futuro CEO")
    edad = st.slider("Edad Cronológica:", 15, 60, 17)
    
    st.markdown("### 🚫 ¿Qué ODIAS?")
    odio_materias = st.multiselect("No me hables de:", ["Matemáticas Avanzadas", "Leer mucha Historia", "Química/Biología", "Hablar en público", "Estar sentado todo el día", "Trabajo físico pesado", "Programación/Código", "Vender/Convencer gente"])
    
    st.markdown("### ❤️ ¿Qué AMAS?")
    hobbies = st.text_area("En tu tiempo libre (Hobbies):", placeholder="Ej: Jugar videojuegos, desarmar cosas, dibujar...")
    
    estilo_trabajo = st.radio("¿Cómo prefieres trabajar?", ["🐺 Lobo Solitario", "🤝 Manada (Equipo)", "⚖️ Híbrido"])
    
    st.markdown("---")
    analizar_btn = st.button("🔮 Generar Futuro Blindado")
    
    if st.button("🔒 Cerrar Sesión"):
        del st.session_state["usuario_activo"]
        st.rerun()

# ==========================================
# 🚀 6. ÁREA PRINCIPAL
# ==========================================
st.title("Quantum Future Path 🏛️")
st.markdown(f"Diseñando la mejor versión profesional para: **{nombre}**")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "assistant", "content": "¡Hola! Soy tu Arquitecto de Vida. Completa el formulario a la izquierda y presiona el botón verde."})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# LÓGICA DEL ANÁLISIS
if analizar_btn:
    if not model:
        st.error("⚠️ Error de Conexión: No se pudo activar el cerebro de la IA. Revisa la API Key en Secrets.")
    else:
        # Prompt mejorado V2
        prompt_sistema = f"""
        ACTÚA COMO: Orientador Vocacional Futurista Senior.
        OBJETIVO: Crear un plan de carrera para {edad} años, resistente a la IA.
        
        PERFIL DEL USUARIO:
        - Lo que AMA (Hobbies): {hobbies}
        - Estilo de trabajo: {estilo_trabajo}
        - 🚫 MATERIAS QUE ODIA/EVITA: {', '.join(odio_materias)}
        
        REGLA DE ORO (EXCLUSIÓN TOTAL):
        Si el usuario seleccionó que ODIA o EVITA un tema, ESTÁ PROHIBIDO sugerir carreras centradas en eso. 
        
        TAREA:
        Genera 3 OPCIONES (1 Universitaria, 1 Técnica/Corta, 1 Oficio Digital/Moderno).
        
        FORMATO DE RESPUESTA PARA CADA OPCIÓN:
        ### [Emoji] Nombre de la Carrera
        * **¿Por qué para ti?**: Conecta sus hobbies con esta carrera.
        * **Escudo Anti-IA**: ¿Por qué un robot no puede hacer esto bien?
        * **Dónde estudiar (México)**: Lugares reales y específicos.
        
        Termina con una frase inspiradora corta.
        """
        
        with st.chat_message("assistant"):
            with st.spinner("Escaneando futuros posibles... 📡"):
                try:
                    response = model.generate_content(prompt_sistema)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "user", "content": "Generar Diagnóstico"})
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    st.session_state.visitas += 1
                    
                    pdf_bytes = generar_pdf_blindado(nombre, "Perfil Completo", response.text)
                    b64 = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Plan_Blindado_{nombre}.pdf" style="text-decoration:none; color: #000000 !important; background-color: #00E676 !important; padding: 15px; border-radius: 10px; display: block; text-align: center; border: 2px solid #000000; font-weight: 800; width: 100%; margin-top: 20px;">📥 DESCARGAR PLAN (PDF)</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error en la Matrix: {e}")

if prompt := st.chat_input("¿Tienes dudas?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        if model:
            resp = model.generate_content(f"Duda vocacional rápida: {prompt}. Recuerda que odia: {', '.join(odio_materias)}")
            st.markdown(resp.text)
            st.session_state.chat_history.append({"role": "assistant", "content": resp.text})
