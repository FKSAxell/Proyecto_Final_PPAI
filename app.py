import streamlit as st

st.set_page_config(
    page_title="Rendimiento Académico Estudiantil",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

rutas ={
    "Proyecto":[
        st.Page("rutas/inicio.py", title="Inicio", icon="🏠"),
        st.Page("rutas/exploracion.py", title="Exploración del Dataset", icon="📊"),
    ]
}
navigate = st.navigation(rutas)
navigate.run()