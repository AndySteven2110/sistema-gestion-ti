import streamlit as st
import requests
import pandas as pd

API = "http://api-gateway:8000/api/proveedores"

st.title("📦 Gestión de Proveedores")

# ================================
#   Obtener proveedores
# ================================
def load_proveedores():
    try:
        resp = requests.get(f"{API}/list")
        return resp.json()
    except:
        return []

proveedores = load_proveedores()

df = pd.DataFrame(proveedores)
st.subheader("Listado de Proveedores")
st.dataframe(df, use_container_width=True)

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

    resp = requests.post(f"{API}/create", json=data)
    if resp.status_code == 200:
        st.success("Proveedor registrado correctamente.")
        st.experimental_rerun()
    else:
        st.error("Error al registrar proveedor.")

st.divider()

# ================================
#   Eliminar proveedor
# ================================
st.subheader("🗑️ Eliminar Proveedor")

proveedores_ids = {f"{p['id']} - {p['razon_social']}": p["id"] for p in proveedores}

sel = st.selectbox("Seleccione un proveedor", list(proveedores_ids.keys()))

if st.button("Eliminar"):
    pid = proveedores_ids[sel]
    requests.delete(f"{API}/delete/{pid}")
    st.success("Proveedor eliminado")
    st.experimental_rerun()
