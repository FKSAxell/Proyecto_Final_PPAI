import streamlit as st
import plotly.express as px
from utils import  NUMERIC_COLS, CATEGORICAL_COLS, es, col_from_es


df = st.session_state.get("df", None)
if df is None:
    st.warning("⚠️ Primero debes cargar el dataset. Ve a la página **Inicio**.")
    st.stop()



st.title("📈 Análisis Univariado")

tab1, tab2 = st.tabs(["🔢 Variables numéricas", "🔤 Variables categóricas"])

with tab1:
    var_num = col_from_es(
        st.selectbox("Selecciona una variable numérica", [es(c) for c in NUMERIC_COLS]),
        NUMERIC_COLS,
    )
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            df, x=var_num, nbins=30,
            title=f"Distribución de {es(var_num)}",
            labels={var_num: es(var_num)},
            color_discrete_sequence=["#4C78A8"],
        )
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.box(
            df, y=var_num,
            title=f"Boxplot de {es(var_num)}",
            labels={var_num: es(var_num)},
            color_discrete_sequence=["#F58518"],
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Estadísticas**")
    stats = df[var_num].describe().round(2)
    st.dataframe(stats.to_frame().T, width="stretch", hide_index=True)

with tab2:
    var_cat = col_from_es(
        st.selectbox("Selecciona una variable categórica", [es(c) for c in CATEGORICAL_COLS]),
        CATEGORICAL_COLS,
    )
    conteo = df[var_cat].value_counts().reset_index()
    conteo.columns = [var_cat, "Cantidad"]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            conteo, x=var_cat, y="Cantidad",
            title=f"Frecuencia de {es(var_cat)}",
            labels={var_cat: es(var_cat)},
            color="Cantidad",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            conteo, names=var_cat, values="Cantidad",
            title=f"Proporción de {es(var_cat)}",
        )
        st.plotly_chart(fig2, use_container_width=True)
