import streamlit as st

from services.auth_service import registrar_usuario

from utils.style_loader import load_css
from utils.hide_st_menu import hide_st_menu

hide_st_menu()

# --- Configuración de la página ---
st.set_page_config(
    page_title="Registro de Usuario",
    layout="centered"
)


load_css("registro.css")


# --- UI ---
st.title("Registro de Usuario")

nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")


# Botones/Acciones

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
    else:
        st.error(mensaje)

if st.button("Volver", ):
    st.switch_page("app.py")

