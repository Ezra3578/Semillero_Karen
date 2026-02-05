import streamlit as st
import json
import os
import streamlit_authenticator as stauth
import re


st.set_page_config(page_title="Registro de Usuario", layout="centered")


ocultar_sidebar = """
    <style>
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
"""
st.markdown(ocultar_sidebar, unsafe_allow_html=True)


estilo_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0EB4F5;
}

/* Centrar el formulario */
.block-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Estilo de la tarjeta */
.block-container > div:first-child {
    background-color: white;
    padding: 2rem 3rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    max-width: 500px;
    width: 100%;
}
</style>
"""
st.markdown(estilo_css, unsafe_allow_html=True)


st.title("Registro de Usuario")

nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")


ruta_json = "data/usuarios.json"


def validar_contrasena(contra):
    if (len(contra) >= 8 and
        re.search(r"[A-Z]", contra) and
        re.search(r"[a-z]", contra) and
        re.search(r"\d", contra) and
        re.search(r"[!@#$%^&*()\\-_=+{}\\[\\]|\\\\;:'\\\",.<>/?]", contra)):
        return True
    return False


if st.button("Registrar"):
    if not all([nombre, correo, usuario, contrasena]):
        st.warning("Por favor completa todos los campos.")
    elif not validar_contrasena(contrasena):
        st.error("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un carácter especial.")
    else:
        hashed_password = stauth.Hasher([contrasena]).generate()[0]

        nuevo_usuario = {
            "nombre": nombre,
            "correo": correo,
            "usuario": usuario,
            "contrasena": hashed_password
        }

        datos = []
        if os.path.exists(ruta_json):
            try:
                with open(ruta_json, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                    if not isinstance(datos, list):
                        datos = []
            except (json.JSONDecodeError, TypeError):
                datos = []

        if any(isinstance(u, dict) and u.get("usuario") == usuario for u in datos):
            st.error("El usuario ya existe. Por favor elige otro nombre de usuario.")
        else:
            datos.append(nuevo_usuario)
            with open(ruta_json, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            st.success("Usuario registrado exitosamente.")