import streamlit as st
from services.session_service import require_login, logout_user, get_user


# --- Configuración ---
st.set_page_config(
    page_title="Inicio",
    layout="wide"
)


# --- Protección ---
require_login()


# --- Usuario actual ---
user = get_user()


# --- Header ---
st.markdown(
    f"""
    <div style="
        background-color: #005B8F;
        padding: 20px;
        border-radius: 12px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <h3 style="margin: 0;">Trazabilidad de Muestras de Agua</h3>
            <p style="margin: 0;">Usuario: {user['usuario']} | Rol: {user['rol']}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


# --- Contenido principal ---
with st.container():
    st.markdown(
        """
        <div style='
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #ddd;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        '>
            <h2 style='color: #005B8F;'>Bienvenido 🎉</h2>
            <p style='font-size: 16px;'>
                El inicio de sesión fue exitoso.<br>
                Desde aquí luego podrás registrar y analizar muestras de agua.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# --- Acciones ---
if st.button("Cerrar sesión"):
    logout_user()
    st.switch_page("app.py")
