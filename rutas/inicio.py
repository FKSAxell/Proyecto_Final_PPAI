import streamlit as st
import pandas as pd


st.title("Inicio")
st.markdown("#### Carga manual")
st.markdown("Sube tu propio archivo CSV:")
uploaded = st.file_uploader(
    "Selecciona un archivo CSV",
    type=["csv"],
    label_visibility="collapsed",
)
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"Archivo **{uploaded.name}** cargado correctamente.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")