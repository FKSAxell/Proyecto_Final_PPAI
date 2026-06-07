import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from utils import  NUMERIC_COLS, CATEGORICAL_COLS, COL_ES, es, col_from_es

df = st.session_state.get("df", None)
if df is None:
    st.warning("⚠️ Primero debes cargar el dataset. Ve a la página **Inicio**.")
    st.stop()



st.title("📊 Análisis Bivariado")

tab1, tab2, tab3 = st.tabs(
    ["🌡️ Correlación numérica", "📦 Categórica vs Puntaje", "🔵 Scatter interactivo"]
)

with tab1:
    st.subheader("Mapa de calor — correlaciones")
    corr = df[NUMERIC_COLS].corr().round(2)
    corr_es = corr.rename(index=COL_ES, columns=COL_ES)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_es, annot=True, fmt=".2f", cmap="coolwarm",
        linewidths=0.5, ax=ax, square=True,
    )
    ax.set_title("Correlación entre variables numéricas")
    st.pyplot(fig)


    corr_exam = corr["Exam_Score"].drop("Exam_Score").sort_values(ascending=False)
    fig2 = px.bar(
        x=corr_exam.values, y=[es(c) for c in corr_exam.index],
        orientation="h",
        title="Correlación de variables con Puntaje de examen",
        color=corr_exam.values,
        color_continuous_scale="RdBu",
        labels={"x": "Correlación", "y": "Variable"},
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    var_cat = col_from_es(
        st.selectbox(
            "Variable categórica vs Puntaje de examen",
            [es(c) for c in CATEGORICAL_COLS],
            key="biv_cat",
        ),
        CATEGORICAL_COLS,
    )
    fig = px.box(
        df, x=var_cat, y="Exam_Score",
        title=f"{es(var_cat)} vs Puntaje de examen",
        labels={var_cat: es(var_cat), "Exam_Score": "Puntaje de examen"},
        color=var_cat,
    )
    st.plotly_chart(fig, use_container_width=True)

    avg = (
        df.groupby(var_cat)["Exam_Score"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("Exam_Score", ascending=False)
    )
    avg.columns = [es(var_cat), "Promedio Puntaje de examen"]
    st.dataframe(avg, width="stretch", hide_index=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        x_var = col_from_es(
            st.selectbox("Eje X", [es(c) for c in NUMERIC_COLS], index=0),
            NUMERIC_COLS,
        )
    with col2:
        color_var = col_from_es(
            st.selectbox("Color (categórica)", [es(c) for c in CATEGORICAL_COLS], index=0),
            CATEGORICAL_COLS,
        )

    fig = px.scatter(
        df, x=x_var, y="Exam_Score",
        color=color_var, opacity=0.6,
        title=f"{es(x_var)} vs Puntaje de examen por {es(color_var)}",
        labels={x_var: es(x_var), "Exam_Score": "Puntaje de examen", color_var: es(color_var)},
        trendline="ols",
    )
    st.plotly_chart(fig, use_container_width=True)
