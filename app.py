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
        st.Page("rutas/exploracion.py", title="Exploración del Dataset", icon="🔍"),
       
    ],
     "Análisis": [
        st.Page("rutas/univariado.py",     title="Análisis Univariado",     icon="📈"),
        st.Page("rutas/bivariado.py",     title="Análisis Bivariado",     icon="📊"),
        st.Page("rutas/factores.py",     title="Factores Clave",     icon="🏆"),
    ],
     "Resultados": [
        st.Page("rutas/conclusiones.py",     title="Conclusiones",     icon="📝"),
     ]
}
def on_click():
    st.session_state.pop("df", None)
    st.session_state.pop("uploaded_filename", None)
    st.success("Dataset limpiado correctamente.")
st.sidebar.button(on_click=on_click, label="Limpiar Dataset", use_container_width=True,disabled=st.session_state.get("df") is None, type="secondary")
navigate = st.navigation(rutas)
navigate.run()