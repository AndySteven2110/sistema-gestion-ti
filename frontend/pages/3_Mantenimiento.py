import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_E = "http://api-gateway:8000/api/equipos"
API_M = "http://api-gateway:8000/api/mantenimientos"

st.title("🛠️ Gestión de Mantenimientos")

# ================================
#   Cargar equipos
# ================================
def load_equipos():
    try:
        return requests.get(f"{API_E}/list").json()
    except:
        return []

equipos = load_equipos()

df_eq = pd.DataFrame(equipos)
st.subheader("Equipos Registrados")
st.dataframe(df_eq, use_container_width=True)

st.divider()

# ================================
#   Formulario registro mantenimiento
# ================================
st.subheader("➕ Registrar Mantenimiento")

with st.form("mnt_form"):
    eq_dict = {f"{e['id']} - {e['marca']} {e['modelo']}": e['id'] for e in equipos}
    equipo_sel = st.selectbox("Equipo", list(eq_dict.keys()))

    tipo = st.selectbox("Tipo", ["Correctivo", "Preventivo"])
    descripcion = st.text_area("Descripción")
    fecha_prog = st.date_input("Fecha Programada")
    fecha_real = st.date_input("Fecha Realizada", None)
    costo = st.number_input("Costo", min_value=0.0, step=10.0)
    tecnico_id = st.number_input("ID Técnico Responsable", min_value=1)
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])

    submit = st.form_submit_button("Registrar")

if submit:
    data = {
        "equipo_id": eq_dict[equipo_sel],
        "tipo": tipo,
        "descripcion": descripcion,
        "fecha_programada": str(fecha_prog),
        "fecha_realizada": str(fecha_real) if fecha_real else None,
        "costo": costo,
        "tecnico_id": int(tecnico_id),
        "prioridad": prioridad
    }

    resp = requests.post(f"{API_M}/", json=data)

    if resp.status_code == 200:
        st.success("Mantenimiento registrado correctamente.")
        st.experimental_rerun()
    else:
        st.error("Error al registrar mantenimiento.")
        st.write(resp.text)

st.divider()

# ================================
#   Listado mantenimientos
# ================================
st.subheader("📋 Mantenimientos Registrados")

try:
    mantenimientos = requests.get(f"{API_M}/").json()
    df_m = pd.DataFrame(mantenimientos)
    st.dataframe(df_m, use_container_width=True)
except:
    st.error("No se pudo obtener mantenimientos.")

st.divider()

# ================================
#   Reporte de costos
# ================================
st.subheader("📊 Reporte de Costos")

if len(mantenimientos) > 0:
    df_cost = pd.DataFrame(mantenimientos)
    df_cost = df_cost[df_cost["costo"] > 0]

    if len(df_cost) > 0:
        fig = px.bar(df_cost, x="id", y="costo", title="Costos de Mantenimientos")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de costos.")
else:
    st.info("No hay registrados.")
