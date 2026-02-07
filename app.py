import streamlit as st
import base64
import pandas as pd
import json
import os
from io import BytesIO
import streamlit as st
import bcrypt

############
from excel.excel_generator import Excel
from pdf.pdf_generator import PDF

from services.auth_service import login
from services.session_service import login_user, is_logged_in

from utils.style_loader import load_css
from utils.hide_st_menu import hide_st_menu

load_css("style.css")

# if "data" not in st.session_state:
#     if os.path.exists("data/muestras.json"):
#         with open("data/muestras.json", "r", encoding="utf-8") as f:
#             st.session_state.data = json.load(f)
#     else:
#         st.session_state.data = []

hide_st_menu()

# === GESTIÓN MULTIUSUARIO ===
# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(page_title="Sistema de Registro de Muestras", layout="wide")
st.markdown("""
    <style>
    div.stButton > button {
        height: 55px !important;      /* Altura uniforme */
        font-size: 16px !important;   /* Tamaño de fuente equilibrado */
        padding: 10px 15px !important;
        white-space: normal !important; /* Permite salto de línea */
        line-height: 1.2 !important;    /* Espaciado correcto entre líneas */
    }
    </style>
""", unsafe_allow_html=True)


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

# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(page_title="Sistema de Registro de Muestras", layout="wide")

# -------------------------
# Inicializar sesión y datos si no existen
# -------------------------
if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "rol" not in st.session_state:
    st.session_state.rol = "usuario"


# -------------------------
# Botón de cerrar sesión
# -------------------------
def cerrar_sesion():
    st.session_state.clear()
    st.success("Sesión cerrada.")
    st.rerun()


# FORMULARIO ANÁLISIS DE LABORATORIO
# -----------------------------------

#Metodo para actualizar las muestras marcadas con estado "Pendiente"
def update_muestras_pendientes():
    st.session_state.muestras_pendientes_fq = {
        m["Código"]: {
            "analizar": m.get("Parámetros a analizar", {}).get("FQ", []),
            "resultados": {}
        }
        for m in st.session_state.data
        if m.get("Estado_FQ") == "pendiente"
    }

    st.session_state.muestras_pendientes_micro = {
        m["Código"]: {
            "analizar": m.get("Parámetros a analizar", {}).get("Micro", []),
            "resultados": {}
        }
        for m in st.session_state.data
        if m.get("Estado_Micro") == "pendiente"
    }


def formulario_analisis_laboratorio():
    # --- Estilo de encabezados en tarjetas ---
    st.markdown("""
        <style>
        .section-title {
            background-color: #f0f4fa; /* azul claro */
            border: 1px solid #d1d9e6;
            border-radius: 8px;
            padding: 28px 24px;
            font-size: 28px;
            font-weight: 600;
            color: #1e3a8a; /* azul oscuro */
            margin-bottom: 20px;
        }
        .save-btn {
            background-color: #1e3a8a; /* azul oscuro */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .save-btn:hover {
            background-color: #0d2a6d; /* azul más oscuro al hover */
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Lista de parámetros y unidades ---
    parametros_fq = [
        "Temperatura","pH","Cloro residual libre","Alcalinidad total","Aluminio residual",
        "Calcio","Cloruros","Color aparente","Conductividad","Dureza total","Fosfato",
        "Hierro total","Magnesio","Nitrito","Sólidos disueltos totales","Sulfatos","Turbiedad",
        "Amonio","DQO","Dureza cálcica","Fenol","Fluoruro","Manganeso","Nitrato","Oxígeno disuelto"
    ]

    parametros_micro = [
       "Coliformes totales", "Escherichia coli", "Mesófilos aerobios"
    ]

    unidades = {
        "Temperatura":"°C","pH":"Unidades","Cloro residual libre":"mg Cl₂/L","Alcalinidad total":"mg CaCO₃/L",
        "Aluminio residual":"mg Al/L","Calcio":"mg Ca/L","Cloruros":"mg Cl/L","Color aparente":"UPC",
        "Conductividad":"µS/cm","Dureza total":"mg CaCO₃/L","Fosfato":"mg PO₄³/L","Hierro total":"mg Fe/L",
        "Magnesio":"mg Mg/L","Nitrito":"mg NO₂/L","Sólidos disueltos totales":"mg/L","Sulfatos":"mg SO₄²/L",
        "Turbiedad":"UNT","Amonio":"mg NH₄⁺/L","DQO":"mg O₂/L","Dureza cálcica":"mg CaCO₃/L",
        "Fenol":"mg C₆H₅OH/L","Fluoruro":"mg F⁻/L","Manganeso":"mg Mn/L","Nitrato":"mg NO₃⁻/L",
        "Oxígeno disuelto":"mg OD/L", "Coliformes totales": "NMP/100mL", "Escherichia coli": "NMP/100mL", 
        "Mesófilos aerobios": "UFC/mL"
    }

    # --- Tabs: Analisis Fisico-Quimico / Analisis Microbiologico ---
    opcion_tipo_analisis = st.radio("Selecciona una opción", ["Análisis Físico-Químicos", "Análisis Microbiológicos"], horizontal=True)

    # --- Inicializar muestras pendientes desde las recepcionadas ---
    if "data" in st.session_state:
        update_muestras_pendientes()

    #PRUEBAS FISICO-QUIMICAS
    if opcion_tipo_analisis == "Análisis Físico-Químicos":
        # --- Encabezado con estilo ---
        st.markdown("<div class='section-title'>Análisis de laboratorio (Físico-químicos)</div>", unsafe_allow_html=True)
        formato_analisis(st.session_state.muestras_pendientes_fq, parametros_fq, unidades, "Estado_FQ")
    elif opcion_tipo_analisis == "Análisis Microbiológicos":
        # --- Encabezado con estilo ---
        st.markdown("<div class='section-title'>Análisis de laboratorio (Microbiológicos)</div>", unsafe_allow_html=True)
        formato_analisis(st.session_state.muestras_pendientes_micro, parametros_micro, unidades, "Estado_Micro")


def formato_analisis(muestras_pendientes, parametros, unidades, tipo_estado):
    # --- Tabs: Muestras por analizar / Muestras analizadas ---
    opcion = st.radio("Selecciona una opción", ["Muestras por analizar", "Muestras analizadas"], horizontal=True)

    clave_resultados = "FQ" if tipo_estado == "Estado_FQ" else "Micro"

    # --- TAB 1: MUESTRAS POR ANALIZAR ---
    if opcion == "Muestras por analizar":

        if not muestras_pendientes:
            st.info("No hay muestras pendientes de análisis.")
            return

        # Selección de muestras
        seleccionadas = st.multiselect(
            "Selecciona las muestras que quieres analizar",
            options=list(muestras_pendientes.keys()),
        )

        if seleccionadas:
            # Encabezado de tabla
            cols = st.columns([2, 1] + [1 for _ in seleccionadas])
            cols[0].markdown("**Ensayo**")
            cols[1].markdown("**Unidades**")
            for i, cod in enumerate(seleccionadas):
                cols[i+2].markdown(f"**{cod}**")

            # Filas de parámetros
            for param in parametros:
                cols = st.columns([2, 1] + [1 for _ in seleccionadas])
                cols[0].write(param)
                cols[1].write(unidades.get(param, ""))

                for i, cod in enumerate(seleccionadas):
                    habilitado = param in muestras_pendientes[cod]["analizar"]
                    key = f"res_{cod}_{param}"

                    if habilitado:
                        valor = cols[i+2].number_input("", key=key, format="%.2f", step=0.01)
                        muestras_pendientes[cod]["resultados"][param] = valor
                    else:
                        cols[i+2].text_input("", value="N/A", disabled=True, key=key)

            # Botones de guardar alineados bajo cada muestra
            cols = st.columns([2, 1] + [1 for _ in seleccionadas])
            cols[0].write("")
            cols[1].write("")
            for i, cod in enumerate(seleccionadas):
                if cols[i+2].button(f"Guardar {cod}", key=f"save_{cod}"):
                    for m in st.session_state.data:
                        if m["Código"] == cod:
                            if "Resultados" not in m:
                                m["Resultados"] = {}    #Inicializacion preventiva de resultados xD

                            m["Resultados"][clave_resultados] = muestras_pendientes[cod]["resultados"]
                            m[tipo_estado] = "analizado"
                            break
                    guardar_datos()
                    muestras_pendientes.pop(cod, None)
                    st.success(f"Muestra {cod} guardada y movida a analizadas.")
                    st.rerun()

    # --- TAB 2: MUESTRAS ANALIZADAS ---
    elif opcion == "Muestras analizadas":
        analizadas = [m for m in st.session_state.data if m.get(tipo_estado) == "analizado"]
        if not analizadas:
            st.info("No hay muestras analizadas aún.")
        else:
            # Encabezado de tabla
            st.markdown("### Muestras analizadas")
            header_cols = st.columns([2, 2, 1])
            header_cols[0].markdown("**Código**")
            header_cols[1].markdown("**# Parámetros**")
            header_cols[2].markdown("**Acciones**")

            for m in analizadas:
                resultados = m.get("Resultados", {}).get(clave_resultados, {})
                cols = st.columns([2, 2, 1])
                cols[0].write(m["Código"])
                cols[1].write(len(resultados))

                # Botón editar
                if cols[2].button(" Editar", key=f"editbtn_{m['Código']}"):
                    st.session_state[f"edit_mode_{m['Código']}"] = True

                # Si está en modo edición
                if st.session_state.get(f"edit_mode_{m['Código']}", False):
                    st.markdown(f"#### Editando resultados de {m['Código']}")

                    # Encabezado
                    cols = st.columns([2, 1, 1])
                    cols[0].markdown("**Ensayo**")
                    cols[1].markdown("**Unidades**")
                    cols[2].markdown("**Valor**")

                    nuevos_resultados = {}
                    for param in parametros:
                        cols = st.columns([2, 1, 1])
                        cols[0].write(param)
                        cols[1].write(unidades.get(param, ""))

                        valor_guardado = resultados.get(param, 0.0)
                        nuevo_valor = cols[2].number_input(
                            "", value=valor_guardado, format="%.2f", step=0.01,
                            key=f"edit_{m['Código']}_{param}"
                        )
                        nuevos_resultados[param] = nuevo_valor

                    # Botón guardar cambios
                    if st.button(" Guardar cambios", key=f"saveedit_{m['Código']}"):
                        m["Resultados"][clave_resultados] = nuevos_resultados
                        guardar_datos()
                        st.session_state[f"edit_mode_{m['Código']}"] = False
                        st.success(f"Resultados de {m['Código']} actualizados")
                        st.rerun()


# -------------------------

def formulario_informacion():
    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 20px; border-radius: 10px; border: 1px solid #d0dfe8; margin-top: 10px;'>
            <h4 style='color: #005B8F;'>Visualización y gestión de muestras</h4>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.data:

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            fuente_filtro = st.selectbox("Fuente de abastecimiento", [""] + sorted(set(m["Fuente"] for m in st.session_state.data)))
        with col2:
            mes_filtro = st.selectbox("Mes", [""] + sorted(set(m["Código"][3:5] for m in st.session_state.data)))
        with col3:
            dia_filtro = st.selectbox("Día", [""] + sorted(set(m["Código"][5:7] for m in st.session_state.data)))
        with col4:
            hora_filtro = st.selectbox("Hora", [""] + sorted(set(m["Hora"] for m in st.session_state.data)))

        # 🔍 Campo de búsqueda por código
        codigo_busqueda = st.text_input("Buscar por código", key="codigo_busqueda")

        filtradas = st.session_state.data

        # Aplicación de filtros
        if codigo_busqueda:
            filtradas = [m for m in filtradas if codigo_busqueda.lower() in m["Código"].lower()]
        if fuente_filtro:
            filtradas = [m for m in filtradas if m["Fuente"] == fuente_filtro]
        if mes_filtro:
            filtradas = [m for m in filtradas if m["Código"][3:5] == mes_filtro]
        if dia_filtro:
            filtradas = [m for m in filtradas if m["Código"][5:7] == dia_filtro]
        if hora_filtro:
            filtradas = [m for m in filtradas if m["Hora"] == hora_filtro]

        if filtradas:
            df = pd.DataFrame(filtradas)
            df["FQ"] = df["Valores FQ"].apply(lambda d: "\n".join([f"{k}: {v}" for k, v in d.items()]))
            df["Micro"] = df["Valores Micro"].apply(lambda d: "\n".join([f"{k}: {v}" for k, v in d.items()]))
            df = df.drop(columns=["Valores FQ", "Valores Micro"])
            st.dataframe(df, use_container_width=True)

            # Botón para descargar Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Resultados")
            st.download_button(
                "Descargar Excel",
                Excel.generar_excel_estilo_laboratorio(filtradas),
                file_name="Resultados_Muestras.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )



            st.markdown("<br>", unsafe_allow_html=True)

            # Botón para descargar PDF
            buffer_pdf = PDF.generar_pdf_masivo(filtradas)
            st.download_button(
                "Descargar resultados en PDF",
                buffer_pdf,
                file_name="resultados_muestras.pdf",
                mime="application/pdf"
            )

            st.markdown("<br>", unsafe_allow_html=True)


            # Sección para eliminar muestra
            codigo_eliminar = st.selectbox("Seleccione la muestra que desea eliminar", [m["Código"] for m in filtradas], key="codigo_a_eliminar")
            if st.checkbox(f"¿Seguro que deseas eliminar {codigo_eliminar}?", key="confirmar_eliminar"):
                if st.button("Eliminar muestra", key="btn_eliminar"):
                    st.session_state.data = [m for m in st.session_state.data if m["Código"] != codigo_eliminar]
                    with open("data/muestras.json", "w", encoding="utf-8") as f:
                        json.dump(st.session_state.data, f, indent=4, ensure_ascii=False)
                    st.success(f"Muestra {codigo_eliminar} eliminada correctamente")
                    st.rerun()
        else:
            st.info("No se encontraron muestras con los filtros aplicados.")



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
            with open("images/EMBALSE.jpg", "rb") as f:
                img = f.read()
                st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.error("No se encontró la imagen 'EMBALSE.jpg'.")

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        try:
            with open("images/LOGO.png", "rb") as f:
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


# Botones según el rol del usuario
if st.session_state.rol == "superusuario":
    # Registro + Recepción + Análisis + Gestión
    boton_col1, boton_col2, boton_col3, boton_col4, boton_col5 = st.columns(5)

    with boton_col1:
        if st.button("Información de Toma de Muestra", use_container_width=True):
            st.session_state.pantalla = "registro"
            st.rerun()

    with boton_col2:
        if st.button(" Información de Recepción de Muestra", use_container_width=True):
            st.session_state.pantalla = "recepcion"
            st.rerun()

    with boton_col3:
        if st.button(" Información de Análisis de Muestra", use_container_width=True):
            st.session_state.pantalla = "analisis"
            st.rerun()

    with boton_col4:
        if st.button(" Consultar Informacion", use_container_width=True):
            st.session_state.pantalla = "informacion"
            st.rerun()

    with boton_col5:
        if st.button(" Gestión de usuarios", use_container_width=True):
            st.session_state.pantalla = "usuarios"
            st.rerun()

elif st.session_state.rol == "toma_muestra":
    # Solo registro
    if st.button(" Registro de muestra", use_container_width=True):
        st.session_state.pantalla = "registro"
        st.rerun()

elif st.session_state.rol == "laboratorio":
    # Solo análisis
    if st.button(" Análisis de laboratorio", use_container_width=True):
        st.session_state.pantalla = "analisis"
        st.rerun()


# Cargar formulario según la pantalla activa
def guardar_datos():
    with open("data/muestras.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, indent=4, ensure_ascii=False)




#-----------------------------------------------------
# visualizacion
#----------------------------------------------------

if "pantalla" in st.session_state:
    if st.session_state.pantalla == "registro":
        pass
    
    elif st.session_state.pantalla == "recepcion":
        pass

    elif st.session_state.pantalla == "analisis":
        formulario_analisis_laboratorio()

    elif st.session_state.pantalla == "informacion":
        formulario_informacion()

    elif st.session_state.pantalla == "usuarios":
        formulario_gestion_usuarios()



