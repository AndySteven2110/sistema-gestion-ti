import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Cargar estilos CSS personalizados
def load_css():
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'styles.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

# Verificar estado de la conexión API
@st.cache_data(ttl=300)  # Cachear por 5 minutos
def check_api_connection():
    try:
        test_response = requests.get(f"{API_URL}/api/health", timeout=5)
        return test_response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Verificar si la API está disponible
api_available = check_api_connection()

# Encabezado con estilo mejorado
st.markdown("""
    <div class="page-header">
        <div class="header-content">
            <h1>📊 Reportes y Análisis</h1>
            <p class="subtitle">Visualiza y analiza los datos del sistema de gestión de TI</p>
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
    /* Estilos para las tarjetas de métricas */
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border-left: 4px solid #6c5ce7;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .metric-card .value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #2d3436;
        margin: 0;
    }
    
    .metric-card .delta {
        font-size: 0.9rem;
        color: #00b894;
        margin: 0.25rem 0 0 0;
    }
    
    .metric-card .delta.negative {
        color: #d63031;
    }
    
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
    
    /* Estilos para los selectores de fecha */
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
        background-color: #6c5ce7 !important;
        border: none !important;
    }
    
    /* Estilos para las tarjetas de gráficos */
    .chart-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .chart-card h3 {
        margin: 0 0 1.5rem 0;
        color: #2d3436;
        font-size: 1.25rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Funciones auxiliares
def get_dashboard_data():
    try:
        response = requests.get(f"{API_URL}/api/reportes/dashboard", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_equipos_por_ubicacion():
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-ubicacion", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_equipos_por_estado():
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-estado", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_equipos_por_categoria():
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-categoria", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_costos_mantenimiento(year=None):
    params = {"year": year} if year else {}
    try:
        response = requests.get(f"{API_URL}/api/reportes/costos-mantenimiento", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_equipos_antiguedad(max_retries=2):
    """
    Obtiene los datos de antigüedad de equipos con manejo de reintentos.
    
    Args:
        max_retries: Número máximo de reintentos en caso de error
        
    Returns:
        dict or None: Los datos de antigüedad o None si hay un error
    """
    url = f"{API_URL}/api/reportes/equipos-antiguedad"
    
    for attempt in range(max_retries + 1):
        try:
            # Mostrar estado del intento
            if attempt > 0:
                st.warning(f"Reintentando... (Intento {attempt + 1}/{max_retries + 1})")
            
            # Hacer la petición con timeout
            response = requests.get(url, timeout=15)
            
            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Verificar si la respuesta tiene el formato esperado
                    if not isinstance(data, (dict, list)):
                        st.warning(f"Formato de respuesta inesperado: {type(data).__name__}")
                        return {'raw': response.text}
                    return data
                except json.JSONDecodeError:
                    # Si no es JSON válido, devolver el texto crudo
                    return {'raw': response.text}
            
            # Si es un error del servidor (5xx), intentar de nuevo
            elif 500 <= response.status_code < 600:
                if attempt == max_retries:
                    st.error(f"Error del servidor (HTTP {response.status_code}). Por favor, intente más tarde.")
                continue
                
            # Otros errores HTTP
            else:
                st.error(f"Error HTTP {response.status_code}: {response.text[:500]}")
                return None
                
        except requests.exceptions.Timeout:
            if attempt == max_retries:
                st.error("Tiempo de espera agotado. El servidor está tardando demasiado en responder.")
            continue
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                st.error(f"Error de conexión: {str(e)}")
            continue
            
        except Exception as e:
            if attempt == max_retries:
                st.error(f"Error inesperado: {str(e)}")
            continue
    
    # Si llegamos aquí, todos los intentos fallaron
    return None

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "📊 Gráficos", "📄 Exportar", "🔍 Análisis Avanzado"])

with tab1:
    st.subheader("Dashboard General")
    
    dashboard = get_dashboard_data()
    
    if dashboard:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📦 Total Equipos",
                value=dashboard.get("total_equipos", 0)
            )
        
        with col2:
            st.metric(
                label="✅ Equipos Operativos",
                value=dashboard.get("equipos_operativos", 0)
            )
        
        with col3:
            st.metric(
                label="🔧 En Reparación",
                value=dashboard.get("equipos_reparacion", 0)
            )
        
        with col4:
            disponibilidad = dashboard.get("tasa_disponibilidad", 0)
            st.metric(
                label="📊 Disponibilidad",
                value=f"{disponibilidad}%",
                delta=f"{disponibilidad - 95:.1f}%"
            )
        
        st.markdown("---")
        
        # Segunda fila
        col1, col2, col3 = st.columns(3)
        
        with col1:
            valor = dashboard.get("valor_inventario", 0)
            st.metric(
                label="💰 Valor Inventario",
                value=f"${valor:,.2f}"
            )
        
        with col2:
            st.metric(
                label="🔧 Mantenimientos (Mes)",
                value=dashboard.get("mantenimientos_mes", 0)
            )
        
        with col3:
            costo = dashboard.get("costo_mantenimiento_mes", 0)
            st.metric(
                label="💵 Costo Mantenim. (Mes)",
                value=f"${costo:,.2f}"
            )
    else:
        st.error("No se pudieron cargar los datos del dashboard")

with tab2:
    st.subheader("Gráficos Estadísticos")
    
    # Equipos por ubicación
    st.markdown("### 📍 Equipos por Ubicación")
    data_ubicacion = get_equipos_por_ubicacion()
    
    if data_ubicacion:
        df_ubicacion = pd.DataFrame(data_ubicacion)
        
        fig1 = px.bar(
            df_ubicacion,
            x='ubicacion',
            y='cantidad',
            title='Distribución de Equipos por Ubicación',
            labels={'ubicacion': 'Ubicación', 'cantidad': 'Cantidad'},
            color='cantidad',
            color_continuous_scale='Blues'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    # Equipos por estado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 Equipos por Estado")
        data_estado = get_equipos_por_estado()
        
        if data_estado:
            df_estado = pd.DataFrame(data_estado)
            
            fig2 = px.pie(
                df_estado,
                values='cantidad',
                names='estado',
                title='Estado Operativo de Equipos',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### 📦 Equipos por Categoría")
        data_categoria = get_equipos_por_categoria()
        
        if data_categoria:
            df_categoria = pd.DataFrame(data_categoria)
            
            fig3 = px.pie(
                df_categoria,
                values='cantidad',
                names='categoria',
                title='Distribución por Categoría',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Costos de mantenimiento
    st.markdown("### 💵 Costos de Mantenimiento")
    
    year_selected = st.selectbox("Seleccionar Año", [2024, 2023, 2022])
    data_costos = get_costos_mantenimiento(year=year_selected)

    if data_costos and isinstance(data_costos, list) and len(data_costos) > 0:
        # Asegurarse de que data_costos sea una lista de diccionarios
        if isinstance(data_costos[0], dict):
            df_costos = pd.DataFrame(data_costos)
            
            if not df_costos.empty:
                # Agrupar por mes
                if 'mes' in df_costos.columns and 'total_costo' in df_costos.columns:
                    df_costos_mes = df_costos.groupby('mes')['total_costo'].sum().reset_index()
                    
                    fig4 = px.line(
                        df_costos_mes,
                        x='mes',
                        y='total_costo',
                        title=f'Costos de Mantenimiento por Mes - {year_selected}',
                        labels={'mes': 'Mes', 'total_costo': 'Costo Total ($)'},
                        markers=True
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                    
                    # Gráfico por tipo
                    if 'tipo' in df_costos.columns:
                        df_costos_tipo = df_costos.groupby('tipo')['total_costo'].sum().reset_index()
                        
                        fig5 = px.bar(
                            df_costos_tipo,
                            x='tipo',
                            y='total_costo',
                            title='Costos por Tipo de Mantenimiento',
                            labels={'tipo': 'Tipo', 'total_costo': 'Costo Total ($)'},
                            color='tipo'
                        )
                        st.plotly_chart(fig5, use_container_width=True)
                else:
                    st.warning("Los datos recibidos no tienen el formato esperado (faltan columnas 'mes' o 'total_costo')")
        else:
            st.warning("Formato de datos inesperado. Se esperaba una lista de diccionarios.")
    else:
        st.info("No hay datos de costos de mantenimiento disponibles para el año seleccionado.")
    
    st.markdown("---")
    
    # Antigüedad de equipos
    st.markdown("### ⏰ Antigüedad de Equipos")
    
    fig6 = None  # Initialize fig6 as None
    with st.expander("🔍 Ver datos crudos", expanded=False):
        data_antiguedad = None
        try:
            st.write("Obteniendo datos de antigüedad de equipos...")
            data_antiguedad = get_equipos_antiguedad()
            
            if data_antiguedad is None:
                st.error("No se pudieron obtener los datos de antigüedad. Por favor, intente más tarde.")
                st.stop()
            
            if not data_antiguedad:
                st.info("No hay datos de antigüedad disponibles.")
                st.stop()
            
            # Check if we got an error message in the response
            if isinstance(data_antiguedad, dict) and 'raw' in data_antiguedad and 'Internal Server Error' in str(data_antiguedad['raw']):
                st.error("Error del servidor al obtener los datos de antigüedad. Por favor, intente más tarde.")
                st.stop()
            
            # Debug: Show raw data in an expander
            with st.expander("Ver datos crudos", expanded=False):
                st.write("Tipo de datos:", type(data_antiguedad))
                st.write("Contenido:", data_antiguedad)
            
            df_antiguedad = None
            
            # Handle different response formats
            if isinstance(data_antiguedad, dict):
                # If it's a dict with a 'data' key
                if 'data' in data_antiguedad:
                    data_antiguedad = data_antiguedad['data']
                # If it's a dict with a 'raw' key that's a string
                elif 'raw' in data_antiguedad and isinstance(data_antiguedad['raw'], str):
                    try:
                        data_antiguedad = json.loads(data_antiguedad['raw'])
                    except json.JSONDecodeError:
                        st.error("No se pudo decodificar la respuesta del servidor.")
                        st.stop()
            # If it's a single record, wrap in a list
            elif all(not isinstance(v, (list, dict)) for v in data_antiguedad.values()):
                data_antiguedad = [data_antiguedad]
            
            # Convert to DataFrame if possible
            if isinstance(data_antiguedad, list) and all(isinstance(x, dict) for x in data_antiguedad):
                df_antiguedad = pd.DataFrame(data_antiguedad)
            elif isinstance(data_antiguedad, dict) and any(isinstance(v, list) for v in data_antiguedad.values()):
                df_antiguedad = pd.DataFrame({k: v for k, v in data_antiguedad.items() if isinstance(v, list)})
            
            if df_antiguedad is not None and not df_antiguedad.empty:
                # Debug: Show DataFrame info in an expander
                with st.expander("Ver estructura del DataFrame", expanded=False):
                    st.write("Columnas:", df_antiguedad.columns.tolist())
                    st.write("Primeras filas:", df_antiguedad.head().to_dict('records'))
                
                # Try to find suitable columns for the plot
                x_col = next((col for col in ['rango_antiguedad', 'rango', 'antiguedad', 'label', 'name', 'categoria'] 
                            if col in df_antiguedad.columns), None)
                y_col = next((col for col in ['cantidad', 'total', 'count', 'value', 'equipos', 'num_equipos'] 
                            if col in df_antiguedad.columns), None)
                
                if x_col and y_col:
                    try:
                        fig6 = px.bar(
                            df_antiguedad,
                            x=x_col,
                            y=y_col,
                            title='Distribución de Equipos por Antigüedad',
                            labels={x_col: 'Antigüedad', y_col: 'Cantidad'},
                            color=y_col,
                            color_continuous_scale='Oranges'
                        )
                        st.plotly_chart(fig6, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al crear el gráfico: {str(e)}")
                else:
                    st.error("No se encontraron las columnas necesarias para generar el gráfico.")
                    st.write("Columnas disponibles:", df_antiguedad.columns.tolist())
            else:
                st.error("No se pudieron procesar los datos para el gráfico.")
                st.json(data_antiguedad)
                
        except Exception as e:
            st.error(f"Error al procesar los datos: {str(e)}")
            if 'data_antiguedad' in locals():
                st.json(data_antiguedad)


# Asegurarse de que las pestañas se rendericen correctamente
with tab3:
        st.subheader("Exportar Reportes")
        
        # Mostrar estado de la conexión
        if not api_available:
            st.warning("⚠️ No se pudo conectar con el servidor. Algunas funciones pueden estar limitadas.")
            st.info("Por favor verifica que el servicio de API esté en ejecución y accesible.")
        else:
            st.success("✅ Conectado al servidor de API")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 Exportar a PDF")
            st.write("Genera un reporte completo en formato PDF")
        
        tipo_reporte_pdf = st.selectbox(
            "Tipo de Reporte (PDF)",
            ["equipos", "mantenimientos", "proveedores"]
        )
        
        if st.button("📥 Generar PDF", use_container_width=True):
            with st.spinner("Generando PDF..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/reportes/export/pdf",
                        json={"type": tipo_reporte_pdf},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            st.success(f"✅ PDF generado: {result.get('filename', 'N/A')}")
                            st.info("El archivo se guardó en el servidor")
                        except json.JSONDecodeError:
                            st.error("Error: La respuesta del servidor no es válida")
                    else:
                        st.error(f"Error al generar PDF: {response.status_code} - {response.text}")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Tiempo de espera agotado. Por favor, intente nuevamente.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")
                except Exception as e:
                    st.error(f"Error inesperado: {str(e)}")
    
with col2:
    st.markdown("### 📊 Exportar a Excel")
    st.write("Genera un reporte detallado en formato Excel")
    
    tipo_reporte_excel = st.selectbox(
        "Tipo de Reporte (Excel)",
        ["equipos", "mantenimientos", "proveedores"]
    )
        
    if st.button("📥 Generar Excel", use_container_width=True):
        with st.spinner("Generando Excel..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/reportes/export/excel",
                    json={"type": tipo_reporte_excel},
                    timeout=30
                )
                    
                if response.status_code == 200:
                    try:
                        result = response.json()
                        st.success(f"✅ Excel generado: {result.get('filename', 'N/A')}")
                        st.info("El archivo se guardó en el servidor")
                    except json.JSONDecodeError:
                        st.error("Error: La respuesta del servidor no es válida")
                else:
                    st.error(f"Error al generar Excel: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                st.error("⏱️ Tiempo de espera agotado. Por favor, intente nuevamente.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")
            except Exception as e:
                st.error(f"Error inesperado: {str(e)}")


    with tab4:
        st.subheader("🔍 Análisis Avanzado")
    
    # Mostrar estado de la conexión
    if not api_available:
        st.warning("⚠️ No se pudo conectar con el servidor. Algunas funciones pueden estar limitadas.")
        st.info("Por favor verifica que el servicio de API esté en ejecución y accesible.")
    else:
        st.success("✅ Conectado al servidor de API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Valor por Categoría")
        try:
            data_categoria = get_equipos_por_categoria()
            
            if not data_categoria:
                st.info("No hay datos disponibles para mostrar el valor por categoría.")
            else:
                try:
                    df_cat = pd.DataFrame(data_categoria)
                    
                    if 'valor_total' in df_cat.columns and not df_cat.empty:
                        fig = go.Figure(data=[go.Bar(
                            x=df_cat['categoria'],
                            y=df_cat['valor_total'],
                            text=df_cat['valor_total'].apply(lambda x: f'${x:,.0f}'),
                            textposition='auto',
                        )])
                        
                        fig.update_layout(
                            title='Valor Total por Categoría',
                            xaxis_title='Categoría',
                            yaxis_title='Valor ($)',
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Los datos no contienen la información necesaria para mostrar el gráfico.")
                except Exception as e:
                    st.error(f"Error al procesar los datos: {str(e)}")
        except Exception as e:
            st.error(f"Error al obtener datos de categorías: {str(e)}")
    
    with col2:
        st.markdown("### 🔧 Eficiencia de Mantenimiento")
        try:
            dashboard = get_dashboard_data()
            
            if not dashboard:
                st.info("No hay datos disponibles para mostrar la eficiencia de mantenimiento.")
            else:
                disponibilidad = dashboard.get("tasa_disponibilidad", 0)
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=disponibilidad,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Tasa de Disponibilidad"},
                    delta={'reference': 95},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 70], 'color': "lightgray"},
                            {'range': [70, 90], 'color': "yellow"},
                            {'range': [90, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 95
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error al obtener datos del dashboard: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 📈 Tendencias")
    with st.expander("Ver más información", expanded=False):
        st.info("""
        ### Próximamente en futuras actualizaciones:
        - Análisis predictivo de fallas
        - Tendencias de mantenimiento
        - Recomendaciones de optimización
        - Pronósticos de costos
        
        Estamos trabajando para ofrecerte estas funcionalidades avanzadas.
        """)

# Footer
st.markdown("---")
st.caption(f"⏰ Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Add error handling at the app level
def main():
    try:
        # The rest of your Streamlit app code would go here
        pass
    except Exception as e:
        st.error(f"Se produjo un error inesperado: {str(e)}")
        st.error("Por favor, intente recargar la página o contacte al administrador si el problema persiste.")

if __name__ == "__main__":
    main()