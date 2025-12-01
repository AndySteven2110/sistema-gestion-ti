import streamlit as st
import requests
import pandas as pd
import os

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
            <h1>🏢 Gestión de Proveedores</h1>
            <p class="subtitle">Administra los proveedores de equipos y servicios de TI</p>
        </div>
    </div>
    <style>
    .page-header {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
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
        background: #6c5ce7 !important;
        color: white !important;
        border-color: #6c5ce7 !important;
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
        background-color: #6c5ce7 !important;
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
        background-color: rgba(108, 92, 231, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ================================
#   Obtener proveedores
# ================================
def load_proveedores():
    try:
        resp = requests.get(f"{API_URL}/api/proveedores", timeout=10)

        if resp.status_code != 200:
            return []

        data = resp.json()

        # CASO 1 → {"proveedores": [...]}
        if isinstance(data, dict) and "proveedores" in data:
            data = data["proveedores"]

        # CASO 2 → Un solo proveedor como diccionario
        if isinstance(data, dict):
            return [data]

        # CASO 3 → Respuesta no es lista
        if not isinstance(data, list):
            return []

        return data

    except Exception as e:
        st.error(f"Error cargando proveedores: {e}")
        return []

proveedores = load_proveedores()

# ================================
#   Tabla de proveedores
# ================================
st.subheader("Listado de Proveedores")

if proveedores:
    df = pd.DataFrame(proveedores)

    # Mostrar solo columnas válidas
    columnas_deseadas = [
        "razon_social", "ruc", "telefono", "email",
        "contacto_nombre", "contacto_telefono", "sitio_web"
    ]

    cols_finales = [c for c in columnas_deseadas if c in df.columns]
    df = df[cols_finales]

    st.dataframe(df, use_container_width=True)
else:
    st.info("No hay proveedores registrados.")

st.divider()

# ================================
#   Registrar proveedor
# ================================
st.subheader("➕ Registrar Nuevo Proveedor")

with st.form("proveedor_form"):
    razon = st.text_input("Razón Social")
    ruc = st.text_input("RUC")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")
    contacto = st.text_input("Persona de Contacto")
    contacto_tel = st.text_input("Teléfono de Contacto")
    sitio_web = st.text_input("Sitio Web")
    notas = st.text_area("Notas")

    submit = st.form_submit_button("Registrar")

if submit:
    data = {
        "razon_social": razon,
        "ruc": ruc,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "contacto_nombre": contacto,
        "contacto_telefono": contacto_tel,
        "sitio_web": sitio_web,
        "notas": notas
    }

    try:
        resp = requests.post(f"{API}/create", json=data, timeout=10)

        if resp.status_code == 200:
            st.success("Proveedor registrado correctamente.")
            st.experimental_rerun()
        else:
            st.error(f"Error al registrar proveedor: {resp.text}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

st.divider()

# ================================
#   Eliminar proveedor
# ================================
st.subheader("🗑️ Eliminar Proveedor")

if proveedores:
    proveedores_ids = {
        f"{p.get('id')} - {p.get('razon_social', 'Sin nombre')}": p.get("id")
        for p in proveedores
        if "id" in p
    }

    sel = st.selectbox("Seleccione un proveedor", list(proveedores_ids.keys()))

    if st.button("Eliminar"):
        pid = proveedores_ids[sel]
        try:
            requests.delete(f"{API}/delete/{pid}", timeout=10)
            st.success("Proveedor eliminado")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error al eliminar proveedor: {e}")
else:
    st.info("No hay proveedores para eliminar.")
