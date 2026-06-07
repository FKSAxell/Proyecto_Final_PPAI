import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import CATEGORICAL_COLS, es


df = st.session_state.get("df", None)
if df is None:
    st.warning("⚠️ Primero debes cargar el dataset. Ve a la página **Inicio**.")
    st.stop()


# ── Título ───────────────────────────────────────────────────────────────────
st.title("📝 Conclusiones")

st.markdown(
    """
    Esta sección sintetiza los hallazgos del análisis exploratorio sobre los
    **6 607 estudiantes** del dataset, respondiendo a la pregunta central:
    > *¿Qué factores determinan realmente el rendimiento académico?*
    """
)

st.markdown("---")

# ── Métricas clave ───────────────────────────────────────────────────────────
NUM_COLS = ["Attendance", "Hours_Studied", "Previous_Scores",
            "Tutoring_Sessions", "Physical_Activity", "Sleep_Hours"]
corr = df[NUM_COLS + ["Exam_Score"]].corr()["Exam_Score"].drop("Exam_Score")

df_q = df.copy()
df_q["q_att"] = pd.qcut(df_q["Attendance"], q=4, labels=["Q1","Q2","Q3","Q4"])
medias_att = df_q.groupby("q_att", observed=True)["Exam_Score"].mean()
brecha_att = medias_att["Q4"] - medias_att["Q1"]

df_q["q_hrs"] = pd.qcut(df_q["Hours_Studied"], q=4, labels=["Q1","Q2","Q3","Q4"])
medias_hrs = df_q.groupby("q_hrs", observed=True)["Exam_Score"].mean()
brecha_hrs = medias_hrs["Q4"] - medias_hrs["Q1"]

impacto_cat = max(
    df.groupby(col)["Exam_Score"].mean().max() - df.groupby(col)["Exam_Score"].mean().min()
    for col in CATEGORICAL_COLS
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Predictor #1", "Asistencia", f"r = {corr['Attendance']:.2f}")
col2.metric("Predictor #2", "Horas de estudio", f"r = {corr['Hours_Studied']:.2f}")
col3.metric("Brecha por asistencia", f"{brecha_att:.1f} pts", "Q4 vs Q1")
col4.metric("Mayor impacto categórico", f"< {impacto_cat:.1f} pts", "todos los grupos")

st.markdown("---")

# ── Hallazgo 1 ───────────────────────────────────────────────────────────────
st.subheader("🔑 Hallazgo 1 — Los factores conductuales dominan el rendimiento")

col_a, col_b = st.columns([1, 1])
with col_a:
    # Gráfico de correlaciones con colores semáforo
    corr_sorted = corr.sort_values(ascending=False)
    colores = ["#2ca02c" if v >= 0.3 else "#ff7f0e" if v >= 0.1 else "#d62728"
               for v in corr_sorted.values]
    fig1 = go.Figure(go.Bar(
        x=corr_sorted.values,
        y=[es(c) for c in corr_sorted.index],
        orientation="h",
        marker_color=colores,
        text=[f"r = {v:+.3f}" for v in corr_sorted.values],
        textposition="outside",
    ))
    fig1.update_layout(
        xaxis_title="Correlación de Pearson (r)",
        xaxis=dict(range=[-0.12, 0.75]),
        margin=dict(l=10, r=80, t=20, b=20),
        height=280,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown(
        """
        Las dos únicas variables con correlación relevante son
        **conductuales**: lo que el estudiante decide hacer cada día.

        | Variable | r | Interpretación |
        |---|---|---|
        | Asistencia | 0.58 | Fuerte |
        | Horas de estudio | 0.45 | Moderada-alta |
        | Puntajes anteriores | 0.18 | Débil |
        | Tutorías | 0.16 | Débil |
        | Actividad física | 0.03 | Nula |
        | Horas de sueño | -0.02 | Nula |

        Las variables de **contexto** (ingreso, tipo de colegio, género)
        tienen correlación efectivamente cero y no aparecen aquí porque
        son categóricas — pero su impacto tampoco supera los 2 puntos.
        """
    )

st.markdown("---")

# ── Hallazgo 2 ───────────────────────────────────────────────────────────────
st.subheader("🔑 Hallazgo 2 — La asistencia genera la mayor brecha observable")

col_c, col_d = st.columns([1, 1])

with col_c:
    st.markdown(
        f"""
        Los estudiantes en el **cuartil más alto de asistencia (Q4)**
        obtienen en promedio **{brecha_att:.1f} puntos más** que los del cuartil más bajo (Q1).
        Esta es la mayor diferencia medible en todo el dataset.

        | Cuartil | Puntaje promedio |
        |---|---|
        | Q1 — Menor asistencia | {medias_att['Q1']:.1f} |
        | Q2 | {medias_att['Q2']:.1f} |
        | Q3 | {medias_att['Q3']:.1f} |
        | Q4 — Mayor asistencia | {medias_att['Q4']:.1f} |

        Asistir regularmente no es solo acumular presencia: implica exposición
        continua al contenido, retroalimentación del docente y práctica guiada —
        experiencias que el estudio independiente no puede replicar completamente.
        """
    )

with col_d:
    fig2 = px.box(
        df_q, x="q_att", y="Exam_Score",
        color="q_att",
        color_discrete_sequence=["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"],
        labels={"q_att": "Cuartil de asistencia", "Exam_Score": "Puntaje de examen"},
        category_orders={"q_att": ["Q1","Q2","Q3","Q4"]},
    )
    fig2.update_layout(showlegend=False, height=320)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Hallazgo 3 ───────────────────────────────────────────────────────────────
st.subheader("🔑 Hallazgo 3 — El contexto socioeconómico tiene impacto mínimo")

impacto = {}
for col in CATEGORICAL_COLS:
    avg = df.groupby(col)["Exam_Score"].mean()
    impacto[col] = round(avg.max() - avg.min(), 3)
imp = pd.Series(impacto).sort_values(ascending=False)

col_e, col_f = st.columns([1.1, 0.9])

with col_e:
    fig3 = px.bar(
        x=imp.values,
        y=[es(c) for c in imp.index],
        orientation="h",
        color=imp.values,
        color_continuous_scale="YlOrRd",
        labels={"x": "Diferencia entre grupos (puntos)", "y": ""},
        text=[f"{v:.2f} pts" for v in imp.values],
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 2.6]),
        margin=dict(l=10, r=80, t=20, b=20),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_f:
    st.markdown(
        """
        Ninguna variable de contexto supera los **2 puntos** de diferencia
        entre sus grupos extremos, en una escala de 0 a 100.

        - **Acceso a recursos** (1.89 pts) e **Involucramiento de padres**
          (1.74 pts) son las más influyentes del grupo, pero su efecto
          es pequeño comparado con los 5.8 pts de la asistencia.
        - **Tipo de colegio** (0.07 pts) y **Género** (0.02 pts) son
          prácticamente irrelevantes como predictores.

        Esto no significa que el contexto no importe en la realidad —
        puede influir indirectamente en la asistencia y el estudio.
        Pero en este dataset, **no explica directamente las diferencias
        de puntaje**.
        """
    )

st.markdown("---")

# ── Recomendaciones ──────────────────────────────────────────────────────────
st.subheader("💡 Recomendaciones basadas en los hallazgos")

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(
        """
        **Priorizar la asistencia**

        Diseñar sistemas de alerta temprana para detectar estudiantes con
        tendencia a ausentarse antes de que el impacto en el puntaje sea
        irreversible. La asistencia es el factor más modificable y de
        mayor efecto.
        """
    )
with r2:
    st.markdown(
        """
        **Fortalecer hábitos de estudio**

        Implementar talleres de técnicas de estudio efectivo. Las horas
        de estudio importan, pero su efecto se maximiza en combinación
        con buena asistencia — ambas variables son complementarias,
        no sustitutas.
        """
    )
with r3:
    st.markdown(
        """
        **No sobreestimar las diferencias de contexto**

        Los datos sugieren que intervenciones orientadas a mejorar
        conductas académicas (asistencia, hábitos de estudio) tienen
        mayor retorno que las que solo actúan sobre el contexto
        socioeconómico sin acompañamiento pedagógico.
        """
    )

st.markdown("---")

# ── Referencias ──────────────────────────────────────────────────────────────
with st.expander("📚 Referencias"):
    st.markdown(
        """
        - Lainguyn (2023). *Student Performance Factors* [Dataset].
          Kaggle. https://www.kaggle.com/datasets/lainguyn123/student-performance-factors

        - Streamlit Inc. (2024). *Streamlit documentation*. https://docs.streamlit.io

        - McKinney, W. (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.

        - Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and
          TensorFlow* (3.ª ed.). O'Reilly Media.

        - Cohen, J. (1988). *Statistical power analysis for the behavioral sciences*
          (2.ª ed.). Lawrence Erlbaum Associates.
        """
    )
