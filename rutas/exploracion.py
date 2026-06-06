import streamlit as st
import pandas as pd

from utils import NUMERIC_COLS, CATEGORICAL_COLS, COL_ES


def _tab_estructura(df):
    st.subheader("Información general")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- **Filas:** {df.shape[0]:,}")
        st.markdown(f"- **Columnas:** {df.shape[1]}")
        st.markdown(f"- **Variables numéricas:** {len(NUMERIC_COLS)}")
        st.markdown(f"- **Variables categóricas:** {len(CATEGORICAL_COLS)}")
    with col2:
        dtype_df = pd.DataFrame({"Variable": df.columns, "Tipo": df.dtypes.values.astype(str)})
        st.dataframe(dtype_df, width="stretch", hide_index=True)


def _tab_estadisticas(df):
    st.subheader("Estadísticas descriptivas — variables numéricas")
    st.dataframe(df[NUMERIC_COLS].describe().T.round(2), width="stretch")


def _tab_categoricas(df):
    st.subheader("Variables categóricas — frecuencias")
    col_sel = st.selectbox(
        "Selecciona una variable",
        options=CATEGORICAL_COLS,
        format_func=lambda c: COL_ES.get(c, c),
    )
    vc = df[col_sel].value_counts().reset_index()
    vc.columns = ["Categoría", "Frecuencia"]
    vc["Porcentaje"] = (vc["Frecuencia"] / len(df) * 100).round(2)
    st.dataframe(vc, hide_index=True, width="stretch")


def _tab_nulos(df):
    st.subheader("Valores nulos por columna")
    nulls = df.isnull().sum().reset_index()
    nulls.columns = ["Variable", "Nulos"]
    nulls["Porcentaje"] = (nulls["Nulos"] / len(df) * 100).round(2)
    if nulls["Nulos"].sum() == 0:
        st.success("✅ El dataset no contiene valores nulos.")
    else:
        st.dataframe(nulls[nulls["Nulos"] > 0], width="stretch")


# --- flujo principal ---

df = st.session_state.get("df", None)
if df is None:
    st.warning("⚠️ Primero debes cargar el dataset. Ve a la página **Inicio**.")
    st.stop()

st.title("🔍 Exploración del Dataset")

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Estructura",
    "📈 Estadísticas descriptivas",
    "🏷️ Variables categóricas",
    "🔎 Valores nulos",
])

with tab1: _tab_estructura(df)
with tab2: _tab_estadisticas(df)
with tab3: _tab_categoricas(df)
with tab4: _tab_nulos(df)
