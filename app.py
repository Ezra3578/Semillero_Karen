import streamlit as st
import base64
import pandas as pd
import json
import streamlit as st
import bcrypt

############

from services.auth_service import login
from services.session_service import login_user, is_logged_in

from utils.style_loader import load_css
from utils.hide_st_menu import hide_st_menu

from images import routes

load_css("style.css")

hide_st_menu()

# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(page_title="Sistema de Registro de Muestras", layout="wide")


# === GESTIÓN MULTIUSUARIO ===
USUARIOS_FILE = "data/usuarios.json"

def cargar_usuarios():
    try:
        with open(USUARIOS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)


# -------------------------
# Inicializar sesión y datos si no existen
# -------------------------
if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "rol" not in st.session_state:
    st.session_state.rol = "usuario"

#######################
def formulario_gestion_usuarios():
    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 25px; border-radius: 10px; border: 1px solid #ccc;'>
            <h3 style='color: #0057A0;'>Gestión de Usuarios</h3>
        </div>
    """, unsafe_allow_html=True)

    usuarios = cargar_usuarios()

    # Mostrar usuarios actuales
    if usuarios:
        st.write("###  Usuarios existentes")
        df_usuarios = pd.DataFrame(usuarios)
        st.dataframe(df_usuarios[["usuario", "correo", "rol"]], use_container_width=True)
    else:
        st.info("No hay usuarios registrados.")

    st.markdown("---")

    # Crear nuevo usuario
    st.write("###  Crear nuevo usuario")
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["superusuario", "toma_muestra", "laboratorio"], key="rol_crear")

    if st.button("Guardar nuevo usuario"):
        if not all([nombre, correo, usuario, contrasena, rol]):
            st.warning(" Por favor completa todos los campos.")
        else:
            # Encriptar la contraseña
            hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

            nuevo_usuario = {
                "nombre": nombre,
                "correo": correo,
                "usuario": usuario,
                "contrasena": hashed,
                "rol": rol
            }

            usuarios.append(nuevo_usuario)
            guardar_usuarios(usuarios)
            st.success(f" Usuario {usuario} creado con rol {rol}")
            st.rerun()

    st.markdown("---")

    # Eliminar usuario
    st.write("###  Eliminar usuario")
    if usuarios:
        user_to_delete = st.selectbox("Selecciona un usuario para eliminar", [u["usuario"] for u in usuarios], key="eliminar_usuario")
        if st.button("Eliminar usuario"):
            usuarios = [u for u in usuarios if u["usuario"] != user_to_delete]
            guardar_usuarios(usuarios)
            st.success(f" Usuario {user_to_delete} eliminado correctamente")
            st.rerun()

    st.markdown("---")

    # Editar usuario existente
    st.write("###  Editar usuario existente")
    if usuarios:
        user_to_edit = st.selectbox("Selecciona un usuario para editar", [u["usuario"] for u in usuarios], key="editar_usuario")

        # Buscar usuario seleccionado
        usuario_obj = next((u for u in usuarios if u["usuario"] == user_to_edit), None)

        if usuario_obj:
            nuevo_nombre = st.text_input("Nombre", value=usuario_obj["nombre"], key=f"nombre_{user_to_edit}")
            nuevo_correo = st.text_input("Correo", value=usuario_obj["correo"], key=f"correo_{user_to_edit}")
            nuevo_rol = st.selectbox(
                "Rol",
                ["superusuario", "toma_muestra", "laboratorio"],
                index=["superusuario", "toma_muestra", "laboratorio"].index(usuario_obj["rol"]),
                key=f"rol_editar_{user_to_edit}"  #  clave única
            )
            nueva_contrasena = st.text_input(
                "Nueva contraseña (dejar en blanco si no deseas cambiarla)", 
                type="password",
                key=f"pass_{user_to_edit}"
            )

            if st.button("Guardar cambios", key=f"guardar_{user_to_edit}"):
                usuario_obj["nombre"] = nuevo_nombre
                usuario_obj["correo"] = nuevo_correo
                usuario_obj["rol"] = nuevo_rol

                if nueva_contrasena.strip() != "":
                    hashed = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()
                    usuario_obj["contrasena"] = hashed

                guardar_usuarios(usuarios)
                st.success(f" Usuario {user_to_edit} actualizado correctamente")
                st.rerun()

# -------------------------
# Login con imagen lateral
# -------------------------
def mostrar_login_con_imagen():
    col1, col2 = st.columns([2, 1])

    with col1:
        try:
            with open(routes.embalse_route, "rb") as f:
                img = f.read()
                st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.error("No se encontró la imagen 'EMBALSE.jpg'.")

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        try:
            with open(routes.logo_empresa_route, "rb") as f:
                logo = f.read()
                logo_b64 = base64.b64encode(logo).decode()
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

# -------------------------
# -------------------------
# Flujo principal
# -------------------------

if not is_logged_in():
    logueado = mostrar_login_con_imagen()

    if logueado:
        st.rerun()
else: 
    st.switch_page("pages/landing.py")


#-----------------------------------------------------
# visualizacion
#----------------------------------------------------

if "pantalla" in st.session_state:
    if st.session_state.pantalla == "registro":
        pass
    
    elif st.session_state.pantalla == "recepcion":
        pass

    elif st.session_state.pantalla == "analisis":
        pass

    elif st.session_state.pantalla == "informacion":
        pass

    elif st.session_state.pantalla == "usuarios":
        formulario_gestion_usuarios()



