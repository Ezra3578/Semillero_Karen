import streamlit as st
from services.auth_service import registrar_usuario


# --- Configuración de la página ---
st.set_page_config(
    page_title="Registro de Usuario",
    layout="centered"
)


# --- Cargar CSS ---
def cargar_css(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


cargar_css("styles/registro.css")


# --- UI ---
st.title("Registro de Usuario")

nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")


# --- Acción ---
if st.button("Registrar"):
    ok, mensaje = registrar_usuario(
        nombre=nombre,
        correo=correo,
        usuario=usuario,
        contrasena=contrasena
    )

    if ok:
        st.success(mensaje)
        st.info("Ahora puedes iniciar sesión.")
        # Opcional:
        # st.switch_page("app.py")
    else:
        st.error(mensaje)
