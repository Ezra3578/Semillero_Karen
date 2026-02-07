import streamlit as st

from services.session_service import require_login, get_user, can

from utils.style_loader import load_css
from utils.hide_st_menu import hide_st_menu

from components.footer import render_footer
from components.header import render_header

hide_st_menu()

# Evitar ingreso sin usuario xD
require_login()


st.set_page_config(
    page_title="Inicio",
    layout="wide"
)

user = get_user()

# Header
render_header()

#Cerrar sesion
def cerrar_sesion():
    st.session_state.clear()
    st.success("Sesión cerrada.")
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔒 Cerrar sesión"):
        cerrar_sesion()

# Acciones
def action_card(title, description, button_text, page):
    load_css("action_card.css")

    st.markdown(
        f"""
        <div class="action-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(button_text, use_container_width=True):
        st.switch_page(page)



# Opciones de acciones
cols = st.columns(2)

index = 0

if can("registrar_muestra"):
    with cols[index % 2]:
        action_card(
            "Registrar muestra",
            "Registrar una nueva muestra tomada en campo.",
            "Registrar",
            "pages/sample_register.py"
        )
    index += 1

if can("recibir_muestra"):
    with cols[index % 2]:
        action_card(
            "Recibir muestra",
            "Registrar la recepción de una muestra en laboratorio.",
            "Recibir",
            "pages/sample_reception.py"
        )
    index += 1

if can("analizar_muestra"):
    with cols[index % 2]:
        action_card(
            "Analizar muestra",
            "Realizar análisis de laboratorio a una muestra.",
            "Analizar",
            "pages/sample_analysis.py"
        )
    index += 1

if can("ver_informacion_muestra"):
    with cols[index % 2]:
        action_card(
            "Información de muestras",
            "Consultar información y trazabilidad de las muestras.",
            "Consultar",
            "pages/sample_information.py"
        )
    index += 1

if can("gestion_usuarios"):
    with cols[index % 2]:
        action_card(
            "Gestión de usuarios",
            "Administrar usuarios y permisos del sistema.",
            "Gestionar",
            "pages/manage_users.py"
        )
    index += 1


#Footer
st.markdown("<br>", unsafe_allow_html=True)
render_footer()
