import streamlit as st


def is_logged_in() -> bool:
    return st.session_state.get("logueado", False)


def get_user():
    return {
        "usuario": st.session_state.get("usuario"),
        "rol": st.session_state.get("rol")
    }


def login_user(usuario: str, rol: str):
    st.session_state.logueado = True
    st.session_state.usuario = usuario
    st.session_state.rol = rol


def logout_user():
    for key in ("logueado", "usuario", "rol"):
        st.session_state.pop(key, None)


def require_login(redirect="app.py"):
    if not is_logged_in():
        st.warning("Debes iniciar sesión.")
        st.switch_page(redirect)


def require_role(rol: str, redirect="app.py"):
    if not is_logged_in():
        st.switch_page(redirect)

    if st.session_state.get("rol") != rol:
        st.error("No tienes permisos para acceder.")
        st.switch_page(redirect)
