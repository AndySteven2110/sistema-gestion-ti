import streamlit as st
import os
import sys
import requests

# Desactivar cualquier configuración de tema
os.environ["STREAMLIT_THEME"] = "light"

# Configuración mínima de la página
st.set_page_config(
    page_title="Sistema de Gestión TI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deshabilitar el tema personalizado
st.markdown("""
    <style>
        /* Reset de estilos de tema */
        :root {
            --primary: #6c5ce7;
            --background-color: #f5f7fa;
            --secondary-background-color: #e6f0ff;
            --text-color: #1a1a1a;
        }
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .main .block-container {
            padding: 2rem 1rem 10rem;
            max-width: 1200px;
        }
    </style>
""", unsafe_allow_html=True)

# URL del API Gateway
API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

# Cargar estilos CSS personalizados
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

def get_dashboard_data():
    try:
        dashboard_url = f"{API_URL}/api/reportes/dashboard"
        st.sidebar.info(f"Intentando conectar a: {dashboard_url}")
        response = requests.get(dashboard_url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.sidebar.error(f"Error en la respuesta del servidor: {response.status_code}")
            st.sidebar.json(response.text[:200])  # Mostrar los primeros 200 caracteres de la respuesta
            return {}
    except Exception as e:
        st.sidebar.error(f"Error al conectar con el servidor: {str(e)}")
        return {}

# Verificar conexión con el servidor
try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        st.sidebar.success("✅ Conectado al servidor")
    else:
        st.sidebar.error("⚠️ No se pudo conectar con el servidor")
except:
    st.sidebar.error("⚠️ Error al conectar con el servidor")

# Título de la aplicación
st.title('Sistema de Gestión TI')


def get_notificaciones():
    try:
        response = requests.get(f"{API_URL}/api/notificaciones", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []


# ======================================
# TITULO PRINCIPAL
# ======================================
st.markdown(
    '''
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
            <div style="font-size: 2.5rem; margin-right: 10px;">🖥️</div>
            <div>
                <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">Sistema de Gestión de Equipos de TI</h1>
                <p style="margin: 0.5rem 0 0; font-size: 1.1rem; opacity: 0.9;">Universidad - Centro de Tecnología de Información</p>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# ======================================
# SIDEBAR
# ======================================
# Reemplazar la sección del logo en el sidebar
with st.sidebar:
    # Logo de la universidad (reemplazado por emoji)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem; font-size: 3rem;">
            💻
        </div>
        <h2 style="text-align: center; margin-bottom: 2rem;">Sistema de TI</h2>
        """, 
        unsafe_allow_html=True
    )

    

    # Información del usuario
    st.markdown(
        """
        <div class="user-info">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <div style="width: 40px; height: 40px; background-color: #e3f2fd; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    <span style="font-size: 1.2rem;">👤</span>
                </div>
                <div>
                    <p style="margin: 0; font-weight: 600; font-size: 1rem;">Administrador</p>
                    <p style="margin: 0; font-size: 0.85rem; color: #6c757d;">admin@universidad.edu</p>
                </div>
            </div>
            <div style="text-align: center; margin-top: 0.5rem;">
                <button style="background: #4a90e2; color: white; border: none; border-radius: 20px; 
                             padding: 0.35rem 1rem; font-size: 0.8rem; cursor: pointer;">
                    Ver perfil
                </button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sección de notificaciones
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 1rem;'>🔔 Notificaciones</h3>", unsafe_allow_html=True)

    # Obtener notificaciones
    raw = get_notificaciones()
    notificaciones = []
    notification_count = 0

    try:
        if isinstance(raw, list):
            notificaciones = raw
        elif isinstance(raw, dict):
            for key in ["notificaciones", "data", "items"]:
                if key in raw and isinstance(raw[key], list):
                    notificaciones = raw[key]
                    break
        elif isinstance(raw, str):
            d = json.loads(raw)
            if isinstance(d, list):
                notificaciones = d
            elif isinstance(d, dict):
                for key in ["notificaciones", "data", "items"]:
                    if key in d and isinstance(d[key], list):
                        notificaciones = d[key]
                        break
    except:
        notificaciones = []
    
    notification_count = len(notificaciones)

    # Mostrar contador de notificaciones
    if notification_count > 0:
        st.markdown(
            f"""
            <div style="position: relative; display: inline-block; margin-bottom: 1rem;">
                <button style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; 
                            padding: 0.5rem 1rem; width: 100%; text-align: left; cursor: pointer;">
                    <span style="font-weight: 600;">Notificaciones</span>
                    <span class="notification-badge">{notification_count if notification_count < 10 else '9+'}</span>
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Mostrar notificaciones
        with st.expander("Ver notificaciones", expanded=False):
            for idx, n in enumerate(notificaciones[:5]):
                time_ago = "hace 2h"  # Esto podría ser dinámico basado en la fecha de la notificación
                st.markdown(
                    f"""
                    <div class="notification-item">
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">
                            {n.get('titulo', 'Sin título')}
                        </div>
                        <div style="font-size: 0.9rem; color: #495057;">
                            {n.get('mensaje', 'Sin mensaje')[:100]}{'...' if len(n.get('mensaje', '')) > 100 else ''}
                        </div>
                        <div class="notification-time">{time_ago}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if idx < len(notificaciones[:5]) - 1:
                    st.markdown("<hr style='margin: 0.5rem 0; border-color: #f1f3f5;'/>", unsafe_allow_html=True)
        
        if notification_count > 5:
            st.markdown(
                f"""
                <div style="text-align: center; margin-top: 0.5rem;">
                    <a href="#" style="color: #4a90e2; text-decoration: none; font-size: 0.85rem;">
                        Ver todas las notificaciones ({notification_count})
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("Sin notificaciones pendientes")

    st.markdown("---")
    st.markdown("### ⚙️ Sistema")

    if st.button("🔄 Ejecutar Agentes"):
        with st.spinner("Ejecutando agentes..."):
            try:
                r = requests.post(f"{API_URL}/api/agents/run-all-agents")
                st.success("Ejecutado correctamente" if r.status_code == 200 else "Error al ejecutar agentes")
            except Exception as e:
                st.error(f"Error: {e}")

# ======================================
# DASHBOARD PRINCIPAL
# ======================================

# Mensaje de bienvenida
st.write('Bienvenido al sistema de gestión de TI. Utilice el menú lateral para navegar entre las diferentes secciones.')

data = get_dashboard_data()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Equipos registrados", data.get('total_equipos', 'N/A'))
with col2:
    st.metric("Mantenimientos pendientes", data.get('mantenimientos_pendientes', 'N/A'))
with col3:
    st.metric("Proveedores activos", data.get('proveedores_activos', 'N/A'))


if data:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📦 Total Equipos", data.get("total_equipos", 0))

    with col2:
        disp = data.get("tasa_disponibilidad", 0)
        st.metric("✅ Disponibilidad", f"{disp}%", delta=f"{disp - 95:.1f}%")

    with col3:
        val = data.get("valor_inventario", 0)
        st.metric("💰 Valor Inventario", f"${val:,.2f}")

    with col4:
        st.metric("🔧 Mantenimientos (Mes)", data.get("mantenimientos_mes", 0))

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🟢 Equipos Operativos", data.get("equipos_operativos", 0))

    with col2:
        st.metric("🔴 En Reparación", data.get("equipos_reparacion", 0))

    with col3:
        c = data.get("costo_mantenimiento_mes", 0)
        st.metric("💵 Costo Mantenim. (Mes)", f"${c:,.2f}")

    st.markdown("---")

    st.markdown("### 📊 Información del Sistema")

    tab1, tab2, tab3 = st.tabs(["🎯 Resumen", "📈 Estadísticas", "ℹ️ Acerca de"])

    with tab1:
        colA, colB = st.columns(2)

        with colA:
            st.markdown("#### Estado del Inventario")
            total = data.get("total_equipos", 1)
            oper = data.get("equipos_operativos", 0)
            rep = data.get("equipos_reparacion", 0)

            st.progress(oper / total if total else 0)
            st.caption(f"Equipos Operativos: {oper}/{total}")

            if rep > 0:
                st.warning(f"⚠️ {rep} equipos en reparación")

        with colB:
            st.markdown("#### Mantenimientos")
            st.info(f"📅 {data.get('mantenimientos_mes', 0)} programados")
            st.info(f"💵 Costo mensual: ${data.get('costo_mantenimiento_mes', 0):,.2f}")

    with tab2:
        st.markdown("#### Métricas Clave")
        st.json({
            "total_equipos": data.get("total_equipos", 0),
            "tasa_disponibilidad": f"{data.get('tasa_disponibilidad', 0)}%",
            "valor_inventario": f"${data.get('valor_inventario', 0):,.2f}",
            "equipos_operativos": data.get("equipos_operativos", 0),
            "equipos_en_reparacion": data.get("equipos_reparacion", 0)
        })

    with tab3:
        st.markdown("""
        ### Sistema de Gestión de Equipos de TI  
        **Versión:** 1.0.0  
        **Última actualización:** Noviembre 2024
        """)

else:
    st.error("⚠️ No se pudo conectar con el servidor.")
    st.info("💡 Ejecute: `docker-compose up -d`")

# ======================================
# FOOTER
# ======================================
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.caption("📧 Soporte: ti@universidad.edu")
with c2:
    st.caption("⏰ Sistema de Gestión TI")
with c3:
    st.caption("🔒 Sistema Seguro")
