import streamlit as st
import pandas as pd

from utils.style_loader import load_css
from utils.hide_st_menu import hide_st_menu

from components.header import render_header
from components.footer import render_footer

from services.session_service import require_login, can, ROLES
from services.user_service import (cargar_usuarios, guardar_usuarios,
                                   crear_usuario, actualizar_usuario,
                                   eliminar_usuario)


hide_st_menu()  #Quitar menú

load_css("laboratory_pages.css") #Cargar CSS

require_login() #Evitar acceso sin login

if not can("gestion_usuarios"):
    st.error("No tienes permisos para acceder a esta sección")
    st.stop()

#Header
render_header()

#Titulo
st.markdown(
    "<div class='titulo-seccion'>Gestión de Usuarios</div>",
    unsafe_allow_html=True
)

#Regresar a la landing page
if st.button("Volver"):
    st.switch_page("pages/landing.py")

def formulario_gestion_usuarios():
    
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
    rol = st.selectbox("Rol", ROLES, key="rol_crear")

    if st.button("Guardar nuevo usuario"):
        if not all([nombre, correo, usuario, contrasena, rol]):
            st.warning(" Por favor completa todos los campos.")
        else:
            usuarios.append(crear_usuario(nombre, correo, usuario, contrasena, rol))    #Crea un usuario
            guardar_usuarios(usuarios)  #Guarda el usuario en el json
            st.success(f" Usuario {usuario} creado con rol {rol}")
            st.rerun()

    st.markdown("---")

    # Eliminar usuario
    st.write("###  Eliminar usuario")
    if usuarios:
        user_to_delete = st.selectbox("Selecciona un usuario para eliminar", 
                                      [u["usuario"] for u in usuarios], 
                                      key="eliminar_usuario")
        if st.button("Eliminar usuario"):
            usuarios = eliminar_usuario(usuarios, user_to_delete)   #Borra el usuario
            guardar_usuarios(usuarios)  #Actualiza el JSON
            st.success(f" Usuario {user_to_delete} eliminado correctamente")
            st.rerun()

    st.markdown("---")

    # Editar usuario existente
    st.write("###  Editar usuario existente")
    if usuarios:
        user_to_edit = st.selectbox("Selecciona un usuario para editar", 
                                    [u["usuario"] for u in usuarios], 
                                    key="editar_usuario")

        # Buscar usuario seleccionado
        usuario_obj = next((u for u in usuarios if u["usuario"] == user_to_edit), None)

        if usuario_obj:
            nuevo_nombre = st.text_input("Nombre", value=usuario_obj["nombre"], key=f"nombre_{user_to_edit}")
            nuevo_correo = st.text_input("Correo", value=usuario_obj["correo"], key=f"correo_{user_to_edit}")
            nuevo_rol = st.selectbox(
                "Rol",
                ROLES,
                index=ROLES.index(usuario_obj["rol"]),
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

                actualizar_usuario(usuario_obj, #Actualiza el usuario
                                   nuevo_nombre, 
                                   nuevo_correo, 
                                   nuevo_rol,  
                                   nueva_contrasena if nueva_contrasena.strip() else None)
                
                guardar_usuarios(usuarios)  #Actualiza el JSON
                st.success(f" Usuario {user_to_edit} actualizado correctamente")
                st.rerun()

formulario_gestion_usuarios()

#Footer
render_footer()