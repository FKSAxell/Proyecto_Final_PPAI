import io

import pandas as pd
import streamlit as st

LOCAL_CSV = "data/StudentPerformanceFactors.csv"


def _cargar_local():
    st.markdown("#### Carga automática")
    st.markdown(f"Usa el archivo local incluido en el proyecto:  \n`{LOCAL_CSV}`")
    if st.button("Cargar dataset local", use_container_width=True, type="primary"):
        try:
            st.session_state["df"] = pd.read_csv(LOCAL_CSV)
            st.success("Dataset cargado correctamente.")
            st.rerun()
        except FileNotFoundError:
            st.error(f"No se encontró el archivo en `{LOCAL_CSV}`.")


def _cargar_manual():
    st.markdown("#### Carga manual")
    st.markdown("Sube tu propio archivo CSV:")
    uploaded = st.file_uploader(
        "Selecciona un archivo CSV",
        type=["csv"],
        label_visibility="collapsed",
        # key=f"file_uploader_{st.session_state.get('uploader_key', 0)}",
    )

    if uploaded is None and st.session_state.get("uploaded_filename") is not None:
        st.session_state.pop("df", None)
        st.session_state.pop("uploaded_filename", None)
        st.rerun()

    if uploaded is not None and st.session_state.get("uploaded_filename") != uploaded.name:
        try:
            df_temp = pd.read_csv(io.BytesIO(uploaded.read()))
            if df_temp.empty:
                st.error("El archivo CSV está vacío.")
            else:
                st.session_state["df"] = df_temp
                st.session_state["uploaded_filename"] = uploaded.name
                st.success(f"Archivo **{uploaded.name}** cargado correctamente ({len(df_temp)} filas).")
                st.rerun()
        except pd.errors.EmptyDataError:
            st.error("El archivo CSV está vacío.")
        except pd.errors.ParserError:
            st.error("Error al parsear el CSV. Verifica el formato del archivo.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {str(e)}")


def _mostrar_contenido():
    st.markdown(
        """
        ### Problemática
        El rendimiento académico de los estudiantes es un fenómeno **multidimensional**
        influenciado por factores personales, familiares, socioeconómicos e institucionales.
        Comprender cuáles son los determinantes más relevantes permite diseñar intervenciones
        educativas más efectivas y focalizadas.

        ### Objetivo general
        Explorar, analizar y visualizar los factores que influyen en el puntaje de examen
        de **6 607 estudiantes**, identificando patrones y variables predictoras clave
        mediante técnicas de Ciencia de Datos.
        """
    )
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    df = st.session_state["df"]
    col1.metric("Estudiantes", f"{len(df):,}")
    col2.metric("Puntaje promedio", f"{df['Exam_Score'].mean():.1f}")
    col3.metric("Puntaje máximo", f"{df['Exam_Score'].max()}")
    col4.metric("Puntaje mínimo", f"{df['Exam_Score'].min()}")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """
            #### Sobre el Dataset
            | Atributo | Detalle |
            |---|---|
            | Fuente | [Kaggle — Student Performance Factors](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors) |
            | Registros | 6 607 |
            | Variables | 20 (7 numéricas · 13 categóricas) |
            | Variable objetivo | Puntaje de examen (0 – 100) |
            """
        )
    with col_b:
        st.markdown(
            """
            #### Cómo usar esta aplicación
            Usa el menú de la izquierda para navegar entre secciones:
            - **Exploración** — estructura y calidad del dataset
           

            """
        )

    st.markdown("---")
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head(10), width="stretch")


# --- flujo principal ---

st.title("🎓 Análisis de Factores de Rendimiento Académico Estudiantil")

if "df" not in st.session_state:
    col_auto, col_manual = st.columns(2)
    with col_auto:
        _cargar_local()
    with col_manual:
        _cargar_manual()
else:
    _mostrar_contenido()
