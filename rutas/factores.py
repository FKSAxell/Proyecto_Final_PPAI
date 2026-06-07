import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import  NUMERIC_COLS, CATEGORICAL_COLS, es

df = st.session_state.get("df", None)
if df is None:
    st.warning("⚠️ Primero debes cargar el dataset. Ve a la página **Inicio**.")
    st.stop()


# ── Contenido ────────────────────────────────────────────────────────────────

# ── Título ───────────────────────────────────────────────────────────────────
st.title("🏆 Factores Clave del Rendimiento Académico")

st.markdown(
    """
    Esta sección identifica qué variables predicen el puntaje de examen,
    separando los factores con **impacto estadísticamente relevante** de los que
    tienen una influencia mínima o prácticamente nula.
    """
)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 1 — Correlación numérica real
# ═══════════════════════════════════════════════════════════════════════════
NUM_SIN_TARGET = [c for c in NUMERIC_COLS if c != "Exam_Score"]
corr_vals = (
    df[NUM_SIN_TARGET + ["Exam_Score"]]
    .corr()["Exam_Score"]
    .drop("Exam_Score")
    .sort_values(ascending=False)
)

st.subheader("📌 1 — ¿Qué variables numéricas predicen el puntaje?")

col1, col2 = st.columns([1.1, 0.9])

with col1:
    colores = ["#2ca02c" if v > 0 else "#d62728" for v in corr_vals.values]
    fig1 = go.Figure(go.Bar(
        x=corr_vals.values,
        y=[es(c) for c in corr_vals.index],
        orientation="h",
        marker_color=colores,
        text=[f"{v:+.3f}" for v in corr_vals.values],
        textposition="outside",
    ))
    fig1.update_layout(
        xaxis_title="Correlación de Pearson (r)",
        yaxis_title="",
        xaxis=dict(range=[-0.15, 0.75]),
        margin=dict(l=10, r=60, t=30, b=30),
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🔍 Interpretación")
    st.info(
        """
        **Asistencia (r = 0.58)** es el predictor numérico más fuerte —
        contrario a la intuición común, supera a las horas de estudio.
        Ir a clases expone al estudiante al contenido, a las explicaciones del
        docente y a la práctica guiada: ese contexto no se recupera solo estudiando.

        **Horas de estudio (r = 0.45)** es el segundo factor: el esfuerzo
        individual importa, pero amplifica sus efectos cuando viene acompañado
        de buena asistencia.

        **Puntajes anteriores (r = 0.18) y tutorías (r = 0.16)** tienen
        influencia moderada-baja: sugieren continuidad en el rendimiento
        y apoyo puntual, pero no son determinantes.

        **Actividad física (r ≈ 0.03) y horas de sueño (r ≈ -0.02)**
        no muestran relación lineal relevante con el puntaje en este dataset.
        """
    )

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 2 — Asistencia en cuartiles vs Puntaje
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("📌 2 — El efecto real de la asistencia")

df2 = df.copy()
df2["Cuartil_Asistencia"] = pd.qcut(
    df2["Attendance"],
    q=4,
    labels=["Q1 — Muy baja", "Q2 — Baja", "Q3 — Alta", "Q4 — Muy alta"],
)

col3, col4 = st.columns([0.9, 1.1])

with col3:
    st.markdown("#### 🔍 Interpretación")
    medias = df2.groupby("Cuartil_Asistencia", observed=True)["Exam_Score"].mean().round(1)
    diferencia = medias.iloc[-1] - medias.iloc[0]

    st.info(
        f"""
        Dividiendo a los estudiantes en cuatro cuartiles de asistencia,
        la diferencia en puntaje promedio entre el grupo de **menor asistencia (Q1)**
        y el de **mayor asistencia (Q4)** es de **{diferencia:.1f} puntos**.

        Esta brecha es la más grande observada en todo el dataset entre cualquier
        par de grupos, lo que confirma a la asistencia como el factor
        **más influyente** del análisis.

        La distribución (boxplot) muestra además que el grupo Q4 tiene menor
        dispersión: los estudiantes que asisten regularmente no solo obtienen
        mejores notas, sino que lo hacen de forma más consistente.
        """
    )
    st.dataframe(
        medias.reset_index().rename(columns={
            "Cuartil_Asistencia": "Grupo de asistencia",
            "Exam_Score": "Puntaje promedio",
        }),
        hide_index=True,
        width="stretch",
    )

with col4:
    fig2 = px.box(
        df2, x="Cuartil_Asistencia", y="Exam_Score",
        color="Cuartil_Asistencia",
        color_discrete_sequence=["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"],
        labels={
            "Cuartil_Asistencia": "Cuartil de asistencia",
            "Exam_Score": "Puntaje de examen",
        },
        title="Distribución del puntaje por cuartil de asistencia",
        category_orders={"Cuartil_Asistencia": ["Q1 — Muy baja", "Q2 — Baja", "Q3 — Alta", "Q4 — Muy alta"]},
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 3 — Horas de estudio vs Puntaje (scatter con tendencia)
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("📌 3 — Horas de estudio: esfuerzo que se refleja en el puntaje")

fig3 = px.scatter(
    df, x="Hours_Studied", y="Exam_Score",
    opacity=0.35,
    trendline="ols",
    trendline_color_override="#d62728",
    labels={
        "Hours_Studied": "Horas de estudio semanales",
        "Exam_Score": "Puntaje de examen",
    },
    title="Relación entre horas de estudio y puntaje de examen (con línea de tendencia)",
    color_discrete_sequence=["#4C78A8"],
)
st.plotly_chart(fig3, use_container_width=True)

st.info(
    """
    **¿Por qué es un factor clave?**

    La línea de tendencia (regresión OLS) confirma una relación positiva y consistente:
    a más horas de estudio, mayor puntaje promedio esperado. La nube de puntos
    muestra dispersión natural (no todos los estudiantes que estudian igual obtienen
    lo mismo), pero la **pendiente positiva es clara y estadísticamente significativa**.

    Un aspecto importante: la relación no es perfecta. Estudiantes con pocas horas
    de estudio pero alta asistencia pueden superar a quienes estudian mucho pero
    asisten poco — esto refuerza que ambos factores son complementarios y no sustitutos.
    """
)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 4 — Impacto real de variables categóricas
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("📌 4 — ¿Cuánto influyen realmente los factores de contexto?")

impacto = {}
for col in CATEGORICAL_COLS:
    avg = df.groupby(col)["Exam_Score"].mean()
    impacto[col] = round(avg.max() - avg.min(), 3)
impacto_s = pd.Series(impacto).sort_values(ascending=False)

col5, col6 = st.columns([1.1, 0.9])

with col5:
    fig4 = px.bar(
        x=impacto_s.values,
        y=[es(c) for c in impacto_s.index],
        orientation="h",
        color=impacto_s.values,
        color_continuous_scale="OrRd",
        labels={"x": "Diferencia de puntaje entre grupos (puntos)", "y": "Variable"},
        title="Diferencia máxima de puntaje promedio entre grupos",
        text=[f"{v:.2f} pts" for v in impacto_s.values],
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 2.5]),
    )
    st.plotly_chart(fig4, use_container_width=True)

with col6:
    st.markdown("#### 🔍 Interpretación")
    st.warning(
        """
        **Hallazgo relevante:** ninguna variable categórica supera los **2 puntos**
        de diferencia entre sus grupos extremos (en una escala de 0 a 100).

        Esto significa que variables como Tipo de colegio (0.07 pts) o Género
        (0.02 pts) son prácticamente **irrelevantes** para predecir el puntaje
        en este dataset.

        Las más influyentes son **Acceso a recursos** (1.89 pts) e
        **Involucramiento de padres** (1.74 pts), pero su efecto sigue siendo
        pequeño comparado con los factores conductuales (asistencia y horas de estudio).

        **Conclusión:** el rendimiento académico en este dataset está explicado
        principalmente por **lo que el estudiante hace** (asistir, estudiar),
        no por su contexto socioeconómico o institucional.
        """
    )
