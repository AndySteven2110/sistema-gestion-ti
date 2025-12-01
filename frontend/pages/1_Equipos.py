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
            <h1>💻 Gestión de Equipos</h1>
            <p class="subtitle">Administra los equipos de cómputo de la universidad</p>
        </div>
    </div>
    <style>
    .page-header {
        background: linear-gradient(135deg, #4a90e2 0%, #5c6bc0 100%);
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

# ================================
#  FUNCIONES AUXILIARES API
# ================================
def normalize_list(response, key_name):
    """
    Convierte correctamente respuestas como:
    - list
    - {"key_name": list}
    - {"data": list}
    """
    if response is None:
        return []

    if isinstance(response, list):
        return response

    if isinstance(response, dict):
        if key_name in response:
            return response[key_name]
        # fallback para cualquier lista dentro del dict
        for v in response.values():
            if isinstance(v, list):
                return v
        return []

    return []


def get_equipos(categoria=None, estado=None):
    params = {}
    if categoria:
        params['categoria'] = categoria
    if estado:
        params['estado'] = estado

    try:
        r = requests.get(f"{API_URL}/api/equipos", params=params, timeout=10)
        if r.status_code == 200:
            return normalize_list(r.json(), "equipos")
    except Exception as e:
        st.error(f"Error: {e}")

    return []


def get_categorias():
    try:
        r = requests.get(f"{API_URL}/api/categorias", timeout=10)
        if r.status_code == 200:
            return normalize_list(r.json(), "categorias")
    except:
        pass
    return []


def get_ubicaciones():
    try:
        r = requests.get(f"{API_URL}/api/ubicaciones", timeout=10)
        if r.status_code == 200:
            return normalize_list(r.json(), "ubicaciones")
    except:
        pass
    return []


def get_proveedores():
    try:
        r = requests.get(f"{API_URL}/api/proveedores", timeout=10)
        if r.status_code == 200:
            return normalize_list(r.json(), "proveedores")
    except:
        pass
    return []


# ================================
#  ESTILOS ADICIONALES
# ================================
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
        background: #4a90e2 !important;
        color: white !important;
        border-color: #4a90e2 !important;
    }
    
    /* Estilos para los formularios */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea,
    .stDateInput>div>div>input {
        border-radius: 8px !important;
        border: 1px solid #ced4da !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Estilos para los botones */
    .stButton>button {
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button.primary {
        background-color: #4a90e2 !important;
        border: none !important;
    }
    
    /* Estilos para las tarjetas */
    .card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Estilos para las tablas */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Efecto hover en filas */
    .stDataFrame tbody tr:hover {
        background-color: rgba(74, 144, 226, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ================================
#  PESTAÑAS
# ================================
tab1, tab2, tab3 = st.tabs(["📋 Lista de Equipos", "➕ Nuevo Equipo", "📊 Estadísticas"])

# ======================================================================
# TAB 1: LISTA DE EQUIPOS
# ======================================================================
# Crear pestañas
tab1, tab2 = st.tabs(["📋 Listado de Equipos", "➕ Nuevo Equipo"])

with tab1:
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="margin: 0 0 1rem 0; color: #2c3e50;">Listado de Equipos</h2>
            <p style="margin: 0; color: #6c757d;">Visualiza y gestiona los equipos del sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tarjeta de filtros
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top: 0; margin-bottom: 1rem; color: #495057;'>🔍 Filtros de Búsqueda</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_categoria = st.selectbox(
                "Categoría",
                ["Todas"] + [c["nombre"] for c in get_categorias()],
                key="filtro_cat"
            )
        with col2:
            filtro_estado = st.selectbox(
                "Estado",
                ["Todos", "operativo", "en_reparacion", "obsoleto", "dado_baja", "en_almacen"],
                key="filtro_est"
            )
        with col3:
            filtro_ubicacion = st.selectbox(
                "Ubicación",
                ["Todas"] + [u["nombre_completo"] for u in get_ubicaciones()],
                key="filtro_ub"
            )
        
        # Botón de búsqueda
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🔍 Aplicar Filtros", use_container_width=True, type="primary"):
                st.experimental_rerun()
        with col2:
            if st.button("🔄 Restablecer", use_container_width=True):
                filtro_categoria = "Todas"
                filtro_estado = "Todos"
                filtro_ubicacion = "Todas"
                st.experimental_rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Obtener equipos --------
    categoria_filtro = filtro_categoria if filtro_categoria != "Todas" else None
    estado_filtro = filtro_estado if filtro_estado != "Todos" else None
    ubicacion_filtro = filtro_ubicacion if filtro_ubicacion != "Todas" else None

    equipos = get_equipos(categoria=categoria_filtro, estado=estado_filtro)

    # -------- Mostrar tabla --------
    if equipos:
        st.success(f"Se encontraron {len(equipos)} equipos")

        # Convertir a DataFrame seguro
        df = pd.DataFrame(equipos)

        columnas_mostrar = [
            "codigo_inventario", "nombre", "marca", "modelo",
            "categoria_nombre", "estado_operativo", "ubicacion_nombre"
        ]
        columnas_validas = [c for c in columnas_mostrar if c in df.columns]

        df_view = df[columnas_validas]

        df_view.rename(columns={
            "codigo_inventario": "Código",
            "nombre": "Nombre",
            "marca": "Marca",
            "modelo": "Modelo",
            "categoria_nombre": "Categoría",
            "estado_operativo": "Estado",
            "ubicacion_nombre": "Ubicación"
        }, inplace=True)

        st.dataframe(df_view, use_container_width=True, height=400)

        # ----------------- DETALLE -----------------
        st.markdown("---")
        st.subheader("Detalle de Equipo")

        # Preparar selectbox robusto para equipos sin código
        opciones_codigos = []
        for e in equipos:
            cod = e.get("codigo_inventario")
            if not cod:
                cod = "(sin código)"
            opciones_codigos.append(cod)

        def format_equipo_codigo(codigo):
            eq = next(
                (x for x in equipos if x.get("codigo_inventario", "(sin código)") == codigo),
                None
            )
            if eq:
                return f"{codigo} - {eq.get('nombre', 'Sin nombre')}"
            return codigo

        equipo_sel = st.selectbox(
            "Seleccionar equipo",
            options=opciones_codigos,
            format_func=format_equipo_codigo
        )

        equipo = next(
            (e for e in equipos 
             if e.get("codigo_inventario", "(sin código)") == equipo_sel),
            None
        )

        # -------- Mostrar detalle --------
        if equipo:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Información General")
                st.write(f"**Código:** {equipo.get('codigo_inventario', 'N/A')}")
                st.write(f"**Nombre:** {equipo.get('nombre', 'N/A')}")
                st.write(f"**Marca:** {equipo.get('marca', 'N/A')}")
                st.write(f"**Modelo:** {equipo.get('modelo', 'N/A')}")
                st.write(f"**Serie:** {equipo.get('numero_serie', 'N/A')}")

            with col2:
                st.markdown("#### Estado")
                estado = equipo.get('estado_operativo', 'N/A')

                if estado == "operativo":
                    st.success(f"🟢 {estado.upper()}")
                elif estado == "en_reparacion":
                    st.warning(f"🟡 {estado.upper()}")
                else:
                    st.error(f"🔴 {estado.upper()}")

                st.write(f"**Categoría:** {equipo.get('categoria_nombre', 'N/A')}")
                st.write(f"**Ubicación:** {equipo.get('ubicacion_nombre', 'N/A')}")

            with col3:
                st.markdown("#### Información Económica")
                st.write(f"**Proveedor:** {equipo.get('proveedor_nombre', 'N/A')}")
                if equipo.get("fecha_compra"):
                    st.write(f"**Fecha Compra:** {equipo['fecha_compra']}")
                if equipo.get("costo_compra"):
                    st.write(f"**Costo:** ${equipo['costo_compra']:,.2f}")
                if equipo.get("fecha_garantia_fin"):
                    st.write(f"**Garantía hasta:** {equipo['fecha_garantia_fin']}")

    else:
        st.info("No se encontraron equipos con los filtros seleccionados")

# ======================================================================
# TAB 2: NUEVO EQUIPO
# ======================================================================
with tab2:
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="margin: 0 0 1rem 0; color: #2c3e50;">Registrar Nuevo Equipo</h2>
            <p style="margin: 0; color: #6c757d;">Completa el formulario para agregar un nuevo equipo al sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        with st.form("form_nuevo_equipo"):
            st.markdown("<h3 style='margin-top: 0; margin-bottom: 1rem; color: #495057;'>📝 Información del Equipo</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)

            # --- Columna 1 ---
            with col1:
                codigo = st.text_input("Código de Inventario*", placeholder="EQ-2024-001")
                nombre = st.text_input("Nombre del Equipo*", placeholder="Laptop Dell Inspiron")
                marca = st.text_input("Marca", placeholder="Dell")
                modelo = st.text_input("Modelo", placeholder="Inspiron 15 3000")

                categorias = get_categorias()
                categoria_id = st.selectbox(
                    "Categoría*",
                    [c["id"] for c in categorias],
                    format_func=lambda x: next((c["nombre"] for c in categorias if c["id"] == x), "")
                )

            # --- Columna 2 ---
            with col2:
                numero_serie = st.text_input("Número de Serie", placeholder="ABC123XYZ")
                fecha_compra = st.date_input("Fecha de Compra", value=date.today())
                costo_compra = st.number_input("Costo de Compra", min_value=0.0, value=0.0, format="%.2f")
                fecha_garantia = st.date_input("Fecha Fin Garantía", value=date.today())

            proveedores = get_proveedores()
            proveedor_id = st.selectbox(
                "Proveedor",
                [None] + [p["id"] for p in proveedores],
                format_func=lambda x: "Ninguno" if x is None else next(
                    (p["razon_social"] for p in proveedores if p["id"] == x), "")
            )

            ubicaciones = get_ubicaciones()
            ubicacion_id = st.selectbox(
                "Ubicación",
                [u["id"] for u in ubicaciones],
                format_func=lambda x: next((u["nombre_completo"] for u in ubicaciones if u["id"] == x), "")
            )

            estado_operativo = st.selectbox(
                "Estado Operativo", 
                ["operativo", "en_reparacion", "obsoleto", "dado_baja", "en_almacen"]
            )
            estado_fisico = st.selectbox(
                "Estado Físico", 
                ["excelente", "bueno", "regular", "malo"]
            )

            notas = st.text_area("Notas / Observaciones")

            submitted = st.form_submit_button("💾 Guardar Equipo", use_container_width=True, type="primary")

        if submitted:
            if not codigo or not nombre:
                st.error("⚠️ Los campos Código y Nombre son obligatorios")
            else:
                nuevo_equipo = {
                    "codigo_inventario": codigo,
                    "nombre": nombre,
                    "marca": marca,
                    "modelo": modelo,
                    "categoria_id": categoria_id,
                    "numero_serie": numero_serie,
                    "fecha_compra": str(fecha_compra),
                    "costo_compra": costo_compra,
                    "fecha_garantia_fin": str(fecha_garantia),
                    "proveedor_id": proveedor_id,
                    "ubicacion_actual_id": ubicacion_id,
                    "estado_operativo": estado_operativo,
                    "estado_fisico": estado_fisico,
                    "notas": notas
                }

                try:
                    r = requests.post(
                        f"{API_URL}/api/equipos",
                        json=nuevo_equipo,
                        timeout=10
                    )
                    if r.status_code == 200:
                        st.success("✅ Equipo registrado exitosamente")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {r.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

# ======================================================================
# TAB 3: ESTADÍSTICAS
# ======================================================================
with tab3:
    st.subheader("Estadísticas de Equipos")

    equipos = get_equipos()
    if equipos:
        df = pd.DataFrame(equipos)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Equipos por Estado")
            if "estado_operativo" in df.columns:
                st.bar_chart(df["estado_operativo"].value_counts())

        with col2:
            st.markdown("#### Equipos por Categoría")
            if "categoria_nombre" in df.columns:
                st.bar_chart(df["categoria_nombre"].value_counts())

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if "costo_compra" in df.columns:
                st.metric("Valor Total Inventario", f"${df['costo_compra'].sum():,.2f}")

        with col2:
            if "ubicacion_nombre" in df.columns:
                st.bar_chart(df["ubicacion_nombre"].value_counts().head(5))
    else:
        st.info("No hay datos para estadísticas.")
