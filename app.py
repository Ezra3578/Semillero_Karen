import streamlit as st
import base64

from services.auth_service import login
from services.session_service import login_user, is_logged_in

from utils.style_loader import load_css
from utils.image_loader import image_to_base64, load_image
from utils.hide_st_menu import hide_st_menu

from images import routes

#Cargar CSS
load_css("style.css")

#Ocultar Menú de St
hide_st_menu()

# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(page_title="Sistema de Registro de Muestras", layout="wide")


# Inicializar sesión y datos si no existen
if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "rol" not in st.session_state:
    st.session_state.rol = "usuario"

#Formulario de Login
def mostrar_login_con_imagen():
    col1, col2 = st.columns([2, 1])

    with col1:
        try:
            img = load_image(routes.embalse_route)
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.error("No se encontró la imagen 'EMBALSE.jpg'.")

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        try:
            logo_b64 = image_to_base64(routes.logo_empresa_route)
            st.markdown(f"""
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{logo_b64}" width="120">
                </div>
            """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("No se encontró el archivo 'LOGO.png'")

        st.markdown('<h4 style="text-align: center;">Iniciar sesión</h4>', unsafe_allow_html=True)

        usuario_input = st.text_input("Usuario")
        contraseña_input = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            ok, msg, data = login(usuario_input, contraseña_input)

            if ok:
                login_user(
                    usuario=data["usuario"],
                    rol=data["rol"]
                )
                st.success(msg)
                return True
            else:
                st.error(msg)

        _, col_centro, _ = st.columns([1, 1.5, 1])  #Centrar el boton de registrarse

        with col_centro:
            if st.button("Registrarse", use_container_width=True):
                st.switch_page("pages/registro.py")


    return False


# Flujo principal
if not is_logged_in():
    logueado = mostrar_login_con_imagen()

    if logueado:
        st.rerun()
else: 
    st.switch_page("pages/landing.py")
