import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import random
from datetime import datetime
#abregar contador
# ==========================================
# ⚙️ 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Quantum Future Path", page_icon="🚀", layout="wide")

# Estilos "Dark Zen" inspirados en tu imagen de referencia
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { background-color: #0E1117 !important; color: #E0E0E0 !important; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    
    /* Inputs del Sidebar */
    .stTextInput > div > div > input { color: white !important; background-color: #0D1117 !important; border: 1px solid #30363D; }
    .stSelectbox > div > div > div { color: white !important; background-color: #0D1117 !important; }
    .stTextArea > div > div > textarea { color: white !important; background-color: #0D1117 !important; }
    
    /* Botones */
    div.stButton > button { 
        background-color: #238636 !important; 
        color: white !important; 
        border: none; 
        border-radius: 6px;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem;
    }
    div.stButton > button:hover { background-color: #2EA043 !important; }

    /* Títulos */
    h1, h2, h3 { color: #E6EDF3 !important; }
    
    /* Chat bubbles */
    div[data-testid="stChatMessage"] { background-color: #161B22 !important; border: 1px solid #30363D; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧠 2. CONEXIÓN CON GEMINI
# ==========================================
# Intenta obtener la clave de st.secrets, si no, usa un placeholder para evitar error al iniciar
api_key = st.secrets.get("GOOGLE_API_KEY")

#if api_key:
    #genai.configure(api_key=api_key)
   # model = genai.GenerativeModel('gemini-2.5-flash')
#else:
    #st.warning("⚠️ Falta configurar la GOOGLE_API_KEY en los Secrets.")
    #model = None

# ==========================================
# 🛠️ 3. FUNCIONES (PDF Y LÓGICA)
# ==========================================

def limpiar_texto(texto):
    """Limpia caracteres para el PDF (Latin-1)"""
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def generar_pdf_blindado(nombre, perfil, analisis):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_fill_color(22, 27, 34) # Color oscuro simulado
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, txt="Quantum Future Path", ln=1, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, txt="Plan de Carrera Blindado contra Obsolescencia", ln=1, align='C')
    pdf.ln(20)
    
    # Datos del Estudiante
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=limpiar_texto(f"Estudiante: {nombre}"), ln=1)
    pdf.cell(0, 10, txt=limpiar_texto(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}"), ln=1)
    pdf.ln(5)
    
    # Análisis de IA
    pdf.set_font("Arial", '', 11)
    # Dividimos el texto largo en líneas
    for linea in analisis.split('\n'):
        # Filtramos negritas de markdown para que se vea limpio
        linea_limpia = linea.replace('**', '').replace('*', '-')
        pdf.multi_cell(0, 7, txt=limpiar_texto(linea_limpia))
        pdf.ln(1)
        
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 🏠 4. INTERFAZ (SIDEBAR - EL FORMULARIO)
# ==========================================

with st.sidebar:
    st.image("logo_quantum.png", use_container_width=True)
    st.title("Parámetros de Diseño")
    st.caption("Configura tu perfil para el análisis.")
    
    # Contador de Visitas Simulado (Para efecto visual inmediato)
    # En una app real usaríamos base de datos, aquí simulamos persistencia simple
    if "visitas" not in st.session_state:
        st.session_state.visitas = random.randint(1200, 1500) # Número inicial "fake"
    st.metric("👀 Estudiantes Orientados", f"{st.session_state.visitas:,}")

    st.markdown("---")
    
    # 1. Datos Básicos
    nombre = st.text_input("Nombre:", "Futuro CEO")
    edad = st.slider("Edad Cronológica:", 15, 60, 17)
    
    # 2. El Filtro Negativo (¡Muy importante!)
    st.markdown("### 🚫 ¿Qué ODIAS?")
    odio_materias = st.multiselect(
        "No me hables de:",
        ["Matemáticas Avanzadas", "Leer mucha Historia", "Química/Biología", 
         "Hablar en público", "Estar sentado todo el día", "Trabajo físico pesado", 
         "Programación/Código", "Vender/Convencer gente"]
    )
    
    # 3. El Filtro de Pasión
    st.markdown("### ❤️ ¿Qué AMAS?")
    hobbies = st.text_area("En tu tiempo libre (Hobbies):", 
                           placeholder="Ej: Jugar videojuegos de estrategia, desarmar cosas, dibujar cómics, organizar fiestas, editar videos en TikTok...")
    
    # 4. Estilo de Trabajo
    estilo_trabajo = st.radio("¿Cómo prefieres trabajar?", 
                              ["🐺 Lobo Solitario (Solo yo y mi tarea)", 
                               "🤝 Manada (Equipo y mucha gente)", 
                               "⚖️ Híbrido (Un poco de ambos)"])
    
    st.markdown("---")
    analizar_btn = st.button("🔮 Generar Futuro Blindado")

# ==========================================
# 🚀 5. ÁREA PRINCIPAL (RESULTADOS)
# ==========================================

st.title("Quantum Future Path 🏛️")
st.markdown(f"Diseñando la mejor versión profesional para: **{nombre}**")

# Estado de la sesión para guardar el chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Mensaje de bienvenida inicial
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "¡Hola! Soy tu Arquitecto de Vida. No te voy a dar consejos aburridos de los 90s. Voy a analizar tus datos contra el mercado laboral de 2030. Completa el formulario a la izquierda y presiona el botón verde."
    })

# Mostrar historial
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# LÓGICA DEL ANÁLISIS
if analizar_btn and model:
    # Construcción del Prompt "Ingeniería de Orientación"
    prompt_sistema = f"""
    ACTÚA COMO: Un Orientador Vocacional Futurista y Experto en Mercado Laboral de México.
    OBJETIVO: Crear un plan de carrera para un joven de {edad} años que sea resistente a la Inteligencia Artificial.
    
    PERFIL DEL USUARIO:
    - Odia/Evita: {', '.join(odio_materias)}
    - Le apasiona (Hobbies): {hobbies}
    - Estilo de trabajo: {estilo_trabajo}
    
    TAREA:
    Analiza su perfil y genera 3 OPCIONES DE CARRERA DISTINTAS (No solo universidad).
    Debes explorar estas ramas:
    1. Opción Universitaria (Licenciatura/Ingeniería).
    2. Opción Técnica/Corta (TSU o Carrera Técnica de 2 años).
    3. Opción "Nueva Economía" (Oficio Moderno, Digital, o Creativo).
    
    PARA CADA OPCIÓN INCLUYE:
    - Nombre de la carrera/rol.
    - 🤖 Nivel de Riesgo ante IA (Bajo/Medio/Alto) y POR QUÉ.
    - 🇲🇽 Dónde estudiar en México (Sé específico: UNAM, IPN, Tec de Monterrey, CONALEP, Universidades Tecnológicas, Platzi, Coursera, CECATI).
    - Por qué hace match con su perfil (Conectalo con sus hobbies).
    
    FORMATO DE SALIDA:
    Usa Markdown limpio. Sé directo, empático pero realista. Al final dame un "Veredicto Quantum" de una frase inspiradora.
    """
    
    # Mostrar spinner mientras piensa
    with st.chat_message("assistant"):
        with st.spinner("Escaneando futuros posibles... 📡"):
            try:
                response = model.generate_content(prompt_sistema)
                texto_respuesta = response.text
                
                st.markdown(texto_respuesta)
                
                # Guardar en historial
                st.session_state.chat_history.append({"role": "user", "content": "Generar Diagnóstico"})
                st.session_state.chat_history.append({"role": "assistant", "content": texto_respuesta})
                
                # Incremento de contador (simulado)
                st.session_state.visitas += 1
                
                # GENERAR PDF
                pdf_bytes = generar_pdf_blindado(nombre, "Perfil Completo", texto_respuesta)
                b64 = base64.b64encode(pdf_bytes).decode()
                
                # Botón de descarga
                href = f'''
                <a href="data:application/octet-stream;base64,{b64}" download="Plan_Blindado_{nombre}.pdf" 
                   style="text-decoration:none; color: #000000 !important; background-color: #00E676 !important; 
                          padding: 15px; border-radius: 10px; display: block; text-align: center; 
                          border: 2px solid #000000; font-weight: 800; width: 100%; margin-top: 20px;">
                   📥 DESCARGAR PLAN BLINDADO (PDF)
                </a>
                '''
                st.markdown(href, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error en la Matrix: {e}")

# Input de chat normal por si quieren preguntar algo más
if prompt := st.chat_input("¿Tienes dudas sobre alguna carrera?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            if model:
                # Prompt de seguimiento (chat normal)
                full_prompt = f"El usuario pregunta sobre su orientación vocacional: {prompt}. Responde brevemente y con enfoque futurista."
                resp = model.generate_content(full_prompt)
                st.markdown(resp.text)
                st.session_state.chat_history.append({"role": "assistant", "content": resp.text})
