import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, date

# Cargar estilos CSS personalizados
def load_css():
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

# Encabezado con estilo mejorado
st.markdown("""
    <div class="page-header">
        <div class="header-content">
            <h1>🔧 Gestión de Mantenimiento</h1>
            <p class="subtitle">Solicita y realiza seguimiento a los mantenimientos de equipos</p>
        </div>
    </div>
    <style>
    .page-header {
        background: linear-gradient(135deg, #00b894 0%, #55efc4 100%);
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
        color: white;
    }
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    .page-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .subtitle {
        margin: 0.5rem 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Estilos adicionales
st.markdown("""
    <style>
    /* Estilos para las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8f9fa;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        border: 1px solid #dee2e6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00b894 !important;
        color: white !important;
        border-color: #00b894 !important;
    }
    
    /* Estilos para las tarjetas */
    .card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Estilos para los botones */
    .stButton>button {
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button.primary {
        background-color: #00b894 !important;
        border: none !important;
    }
    
    /* Estilos para las tablas */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Efecto hover en filas */
    .stDataFrame tbody tr:hover {
        background-color: rgba(0, 184, 148, 0.1) !important;
    }
    
    /* Estilos para los estados */
    .estado-pendiente { color: #f39c12; font-weight: 500; }
    .estado-en-proceso { color: #3498db; font-weight: 500; }
    .estado-completado { color: #2ecc71; font-weight: 500; }
    .estado-cancelado { color: #e74c3c; font-weight: 500; }
    
    /* Estilos para las tarjetas de resumen */
    .card-estadistica {
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .card-estadistica h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .card-estadistica p {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
#   Función segura para cargar equipos desde API
# =====================================================
def load_equipos():
    try:
        response = requests.get(f"{API_URL}/api/equipos", timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()

        # Caso API devuelve {"equipos": [...]}
        if isinstance(data, dict) and "equipos" in data:
            data = data["equipos"]

        # Si devuelve un solo equipo como dict → convertir a lista
        if isinstance(data, dict):
            data = [data]

        # Asegurar que sea lista
        if not isinstance(data, list):
            return []

        # Filtrar solo dicts válidos
        return [e for e in data if isinstance(e, dict)]
    except Exception as e:
        st.error(f"Error al cargar equipos: {e}")
        return []

equipos = load_equipos()

# =====================================================
#   Mostrar tabla de equipos
# =====================================================
if not equipos:
    st.info("No hay equipos registrados.")
else:
    df_eq = pd.DataFrame(equipos)
    st.subheader("Equipos Registrados")
    st.dataframe(df_eq, use_container_width=True)

st.divider()

# =====================================================
#   Formulario para registrar mantenimiento
# =====================================================
st.subheader("➕ Registrar Mantenimiento")

# Construir diccionario seguro para el selectbox
equipo_dict = {}
for e in equipos:
    label = f"{e.get('id', '???')} - {e.get('marca', 'Sin marca')} {e.get('modelo', '')}"
    equipo_dict[label] = e.get("id")

if not equipo_dict:
    st.error("No hay equipos disponibles para registrar mantenimientos.")
    st.stop()

with st.form("mnt_form"):
    # Campos del formulario
    equipo_sel = st.selectbox("Equipo", list(equipo_dict.keys()))
    tipo = st.selectbox("Tipo", ["Correctivo", "Preventivo"])
    descripcion = st.text_area("Descripción")
    fecha_prog = st.date_input("Fecha Programada")
    fecha_real = st.date_input("Fecha Realizada", None)
    costo = st.number_input("Costo", min_value=0.0, step=10.0)
    tecnico_id = st.number_input("ID Técnico Responsable", min_value=1)
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
    
    # Botón de envío del formulario
    submitted = st.form_submit_button("💾 Registrar Mantenimiento", use_container_width=True, type="primary")

# Procesar el formulario después de que se envía
if submitted:
    data = {
        "equipo_id": equipo_dict[equipo_sel],
        "tipo": tipo,
        "descripcion": descripcion,
        "fecha_programada": str(fecha_prog),
        "fecha_realizada": str(fecha_real) if fecha_real else None,
        "costo": costo,
        "tecnico_id": int(tecnico_id),
        "prioridad": prioridad
    }

    try:
        resp = requests.post(f"{API_URL}/api/mantenimientos", json=data, timeout=10)
        if resp.status_code == 200:
            st.success("✅ Mantenimiento registrado correctamente.")
            st.rerun()
        else:
            st.error(f"❌ Error al registrar mantenimiento: {resp.text}")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

st.divider()

# =====================================================
#   Listado de mantenimientos
# =====================================================
st.subheader("📋 Mantenimientos Registrados")

def load_mantenimientos():
    try:
        resp = requests.get(f"{API_URL}/api/mantenimientos", timeout=10)
        if resp.status_code != 200:
            return []

        data = resp.json()

        if isinstance(data, dict) and "mantenimientos" in data:
            data = data["mantenimientos"]

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            return []

        return data
    except:
        return []

mantenimientos = load_mantenimientos()

if mantenimientos:
    df_m = pd.DataFrame(mantenimientos)
    st.dataframe(df_m, use_container_width=True)
else:
    st.info("No hay mantenimientos registrados.")

st.divider()

# =====================================================
#   Reporte de costos
# =====================================================
st.subheader("📊 Reporte de Costos")

if mantenimientos:
    df_cost = pd.DataFrame(mantenimientos)

    # ----------- FIX CRÍTICO --------------
    # Si no existe la columna costo → crearla en 0
    if "costo" not in df_cost.columns:
        df_cost["costo"] = 0

    # Eliminar registros sin costo
    df_cost = df_cost[df_cost["costo"] > 0]

    if not df_cost.empty:
        fig = px.bar(df_cost, x="id", y="costo", title="Costos de Mantenimientos")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de costos.")
else:
    st.info("No hay registrados.")
