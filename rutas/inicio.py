import streamlit as st
import pandas as pd

LOCAL_CSV="data/StudentPerformanceFactors.csv"
df=None
st.title("Inicio")


col_auto, col_manual = st.columns(2)
with col_auto:
    st.markdown("#### Carga automática")
    st.markdown(
        f"Usa el archivo local incluido en el proyecto:  \n`{LOCAL_CSV}`"
    )
    if st.button("Cargar dataset local", use_container_width=True, type="primary"):
        try:
            df = pd.read_csv(LOCAL_CSV)
            st.success("Dataset cargado correctamente.")
        except FileNotFoundError:
            st.error(f"No se encontró el archivo en `{LOCAL_CSV}`.")


with col_manual:
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


if df is not None:
    st.markdown("### Vista previa del dataset")
    st.dataframe(df.head())