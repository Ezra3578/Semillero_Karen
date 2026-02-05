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


with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "data" not in st.session_state:
    if os.path.exists("data/muestras.json"):
        with open("data/muestras.json", "r", encoding="utf-8") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = []

st.markdown("""
    <style>
        /* Oculta completamente el menú lateral y su espacio */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Expande el contenido a todo el ancho */
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 0rem;
        }

        /* Oculta el botón hamburguesa (≡) */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Ocultar el menú lateral y el ícono de Streamlit
st.markdown("""
    <style>
        /* Ocultar menú lateral */
        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* Ocultar botón de menú (hamburguesa) */
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
    

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
#Convertir imagen a base64
# -------------------------
def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
logo_floter = image_to_base64("images/logo_floter.png")  

# -------------------------
# Header con logos
# -------------------------
def mostrar_header_doble():

    with open("images/LOGO USTA.png", "rb") as f1, open("images/LOGO.png", "rb") as f2, open("images/NOMBRE LOGO.png", "rb") as f3:
        logo_usta = base64.b64encode(f1.read()).decode()
        logo_empresa = base64.b64encode(f2.read()).decode()
        logo_nombre = base64.b64encode(f3.read()).decode()

    st.markdown(f"""
        <!-- Franja superior gris -->
        <div style="background-color: #e5e5e5; padding: 5px 30px; display: flex; align-items: center; justify-content: flex-end;">
            <img src="data:image/png;base64,{logo_usta}" style="height: 60px;">
        </div>

        <!-- Franja inferior con logos de empresa y texto -->
        <div style="background-color: white; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="data:image/png;base64,{logo_empresa}" style="height: 70px;">
                <div style="border-left: 2px solid #ccc; height: 60px;"></div>
                <img src="data:image/png;base64,{logo_nombre}" style="height: 70px;">
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="border-left: 2px solid #ccc; height: 60px;"></div>
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                    padding-left: 20px;
                ">
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        color: #0057A0;
                        font-family: 'Segoe UI Semibold', 'Segoe UI', sans-serif;
                        letter-spacing: 1.2px;
                        line-height: 1.1;
                        text-align: center;
                    ">
                        Sistema de registro de<br>muestras
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# Botón de cerrar sesión
# -------------------------
def cerrar_sesion():
    st.session_state.clear()
    st.success("Sesión cerrada.")
    st.rerun()
    
#--------------------------
# FORMULARIO RECEPCIÓN MUESTRA
#-------------------------
def formulario_recepcion_muestra():

    # ================================
    # 1. ESTILOS GLOBAL PARA LA SECCIÓN
    # ================================
    st.markdown("""
    <style>
        /* Caja de título */
        .titulo-seccion {
            background-color: #f0f4fa;
            border: 1px solid #d1d9e6;
            border-radius: 8px;
            padding: 22px 24px;
            font-size: 26px;
            font-weight: 600;
            color: #1e3a8a;
            margin-bottom: 20px;
        }

        /* Botones tipo pestaña */
        .stButton button {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border: 2px solid #ffffff !important;
            border-radius: 10px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 10px 16px !important;
            width: 100% !important;
        }

        /* Efecto hover */
        .stButton button:hover {
            background-color: #e8f0fe !important;
        }

        /* Botón activo */
        .active-btn button {
            background-color: #1e3a8a !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if "tab_recepcion" not in st.session_state:
        st.session_state.tab_recepcion = "nuevas"

    # ================================
    # 2. TÍTULO PRINCIPAL
    # ================================
    st.markdown('<div class="titulo-seccion">Recepción de muestra</div>', unsafe_allow_html=True)

    # ================================
    # 3. BOTONES DE NAVEGACIÓN
    # ================================
    col1, col2 = st.columns([1, 1])

    with col1:
        btn1 = st.button("Recepción de muestra")
    with col2:
        btn2 = st.button("Muestras recepcionadas")

    # Actualizar vista
    if btn1:
        st.session_state.tab_recepcion = "nuevas"
    elif btn2:
        st.session_state.tab_recepcion = "recepcionadas"

    # Aplicación visual de botón activo
    if st.session_state.tab_recepcion == "nuevas":
        st.markdown('<div class="active-btn"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div></div>', unsafe_allow_html=True)

    # ================================
    # 4. LISTAS DE PARÁMETROS
    # ================================
    parametros_fq = [
        "Temperatura", "pH", "Cloro residual libre", "Alcalinidad total", "Aluminio residual",
        "Calcio", "Cloruros", "Color aparente", "Conductividad", "Dureza total", "Fosfato",
        "Hierro total", "Magnesio", "Nitrito", "Sólidos disueltos totales", "Sulfatos", "Turbiedad",
        "Amonio", "DQO", "Dureza cálcica", "Fenol", "Fluoruro", "Manganeso", "Nitrato", "Oxígeno disuelto"
    ]

    parametros_micro = ["Coliformes totales", "Escherichia coli", "Mesófilos aerobios"]

    correcciones = {"Cloro residual": "Cloro residual libre"}

    # ================================
    # 5. TAB: NUEVAS RECEPCIONES
    # ================================
    if st.session_state.tab_recepcion == "nuevas":
        pendientes = [m for m in st.session_state.data if "Fecha Recepción" not in m]

        if not pendientes:
            st.info("No hay muestras pendientes de recepción.")
        else:
            codigo = st.selectbox("Seleccione la muestra registrada", [m["Código"] for m in pendientes])
            muestra = next(m for m in pendientes if m["Código"] == codigo)

            fecha_recepcion = st.date_input("Fecha de recepción")
            hora_recepcion = st.time_input("Hora de recepción")
            temperatura_recepcion = st.number_input("Temperatura de recepción (°C)", format="%.2f")
            persona_recepciona = st.text_input("Recepciona (nombre)")

            st.markdown("---")

            seleccion_fq = st.multiselect(
                "Parámetros físico-químicos",
                parametros_fq,
                key=f"new_fq_{codigo}"
            )

            seleccion_micro = st.multiselect(
                "Parámetros microbiológicos",
                parametros_micro,
                key=f"new_micro_{codigo}"
            )

            if st.button("Guardar recepción"):
                muestra["Fecha Recepción"] = fecha_recepcion.strftime("%Y-%m-%d")
                muestra["Hora Recepción"] = hora_recepcion.strftime("%H:%M")
                muestra["Temperatura Recepción"] = temperatura_recepcion
                muestra["Recepcionó"] = persona_recepciona
                muestra["Parámetros a analizar"] = {"FQ": seleccion_fq, "Micro": seleccion_micro}
                muestra["Estado_FQ"] = "pendiente"
                muestra["Estado_Micro"] = "pendiente"
                guardar_datos()
                st.success(f"Muestra {codigo} recepcionada con éxito")
                st.rerun()

    # ================================
    # 6. TAB: RECEPCIONADAS
    # ================================
    elif st.session_state.tab_recepcion == "recepcionadas":
        recepcionadas = [m for m in st.session_state.data if "Fecha Recepción" in m]

        if not recepcionadas:
            st.info("No hay muestras recepcionadas.")
        else:
            for muestra in recepcionadas:
                with st.expander(f"Muestra {muestra['Código']}"):
                    st.write(f"Recepcionada por: {muestra.get('Recepcionó', '')}")

                    valores_guardados_fq = muestra.get("Parámetros a analizar", {}).get("FQ", [])
                    valores_guardados_micro = muestra.get("Parámetros a analizar", {}).get("Micro", [])

                    seleccion_fq = st.multiselect(
                        "Parámetros físico-químicos",
                        parametros_fq,
                        default=[v for v in valores_guardados_fq if v in parametros_fq],
                        key=f"edit_fq_{muestra['Código']}"
                    )

                    seleccion_micro = st.multiselect(
                        "Parámetros microbiológicos",
                        parametros_micro,
                        default=[v for v in valores_guardados_micro if v in parametros_micro],
                        key=f"edit_micro_{muestra['Código']}"
                    )

                    if st.button(f"Guardar cambios {muestra['Código']}"):
                        muestra["Parámetros a analizar"]["FQ"] = seleccion_fq
                        muestra["Parámetros a analizar"]["Micro"] = seleccion_micro
                        guardar_datos()
                        st.success(f"Parámetros de {muestra['Código']} actualizados")
                        st.rerun()

#------------------------------------------------------------
# REGISTRO MUESTRA
def formulario_registro_muestra():
    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 25px; border-radius: 10px; border: 1px solid #ccc;'>
            <h3 style='color: #0057A0;'>Registro de Muestra</h3>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if "puntos_red" not in st.session_state:
        st.session_state["puntos_red"] = [
        "San Cristóbal", "Silveria Espinoza", "Santa Rita", "Copihue", "Alcaldía",
        "Girardot", "Arboleda", "Manablanca", "Carcel de la policia", "Batallón",
        "Universidad", "Coliseo", "Brasilia", "Hospital", "SENA", "Prado",
        "Pueblo Viejo", "Villa Olímpica"]
    
    with col1:
        tipo_muestra = st.selectbox("Tipo de Muestra", ["", "Interna", "Red", "Externa"])
        
        codigo_punto_red = ""
        if tipo_muestra == "Red":
            opciones_red = st.session_state["puntos_red"] + ["Crear nuevo punto de red"]
            seleccion = st.selectbox("Código del punto de red", [""] + opciones_red)


            if seleccion == "Crear nuevo punto de red":
                nuevo_punto = st.text_input("Ingrese el nuevo código del punto de red")
                if nuevo_punto:
                    if nuevo_punto not in st.session_state["puntos_red"]:
                        st.session_state["puntos_red"].append(nuevo_punto)
                    codigo_punto_red = nuevo_punto
            elif seleccion:
                codigo_punto_red = seleccion
        fecha = st.date_input("Fecha")
        quien_muestrea = st.text_input("Persona que Tomó la Muestra")          
        dispositivo = st.selectbox("Dispositivo de Toma de Muestra", ["", "Manguera", "Canal", "Grifo", "Otro"])       
        if dispositivo == "Otro":
            dispositivo_otro = st.text_input("Especifique el dispositivo")
            dispositivo = dispositivo_otro if dispositivo_otro else dispositivo
        tipo_agua = st.selectbox("Tipo de Agua", ["", "Agua potable (AP)", "Agua superficial (ASP)", "Agua subterránea (ASB)", "Agua envasada (AE)", "Agua lluvia (AL)",  "Otra (O)"])
        if tipo_agua == "Otra (O)":
            tipo_agua_otro = st.text_input("Especifique el tipo de agua")
            tipo_agua = tipo_agua_otro if tipo_agua_otro else tipo_agua 
    with col2:
        hora = st.time_input("Hora")  
        fuente = st.selectbox ("Fuente de Abastecimiento", ["", "Andes Medio", "Mancilla Bajo", " Botello Alto", "San Rafael I", "San Rafael II", "Deudoro Aponte", "Manablanca","Cartagenita","Guapucha II","Gatillo 0","Gatillo 1", "Gatillo 2","Gatillo 3"])
        observaciones = st.text_area("Observaciones")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 25px; border-radius: 10px; border: 1px solid #ccc;'>
               <h3 style='color: #0057A0;'>Datos In Situ</h3>
        </div>
  """, unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)
    with col3:
        ph = st.number_input("pH", format="%.2f", step=0.01)
    with col4:
        cloro = st.number_input("Cloro (mg/L)", format="%.2f", step=0.01)
    with col5:
        temperatura = st.number_input("Temperatura (°C)", format="%.2f", step=0.01)

    st.markdown("<br>", unsafe_allow_html=True)

    guardar = st.button("Guardar muestra", use_container_width=True)
    if guardar:
        # === VALIDACIÓN DE CAMPOS OBLIGATORIOS ===
        campos_obligatorios = [
            fecha, quien_muestrea.strip(), dispositivo, tipo_agua, hora, fuente
        ]
        if tipo_muestra == "Red":
            campos_obligatorios.append(codigo_punto_red.strip())

        if not all(campos_obligatorios):
            st.warning(" Por favor, completa todos los campos antes de continuar.")
            return


        #Creacion ID unico
        fecha_codigo = fecha.strftime('%y%m%d')
        existentes = [row["Código"] for row in st.session_state.data if row["Código"][1:7] == fecha_codigo]
        numeros_existentes = [int(cod[7:]) for cod in existentes]
        siguiente = max(numeros_existentes, default=0) + 1
        letra_fuente = "I" if tipo_muestra=="Interna"  else ("R" if tipo_muestra == "Red" else "E")
        codigo = f"{letra_fuente}{fecha_codigo}{siguiente:03d}"

        nueva_muestra = {
            "Código": codigo,
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Hora": hora.strftime("%H:%M"),
            "Quién Muestra": quien_muestrea,
            "Dispositivo": dispositivo,
            "Fuente": fuente,
            "Código Red": codigo_punto_red,
            "Tipo Agua": tipo_agua,
            "pH": ph,
            "Cloro": cloro,
            "Temperatura": temperatura,
            "Observaciones": observaciones,
            "Valores FQ": {},
            "Valores Micro": {}
        }

        st.session_state.data.append(nueva_muestra)
        guardar_datos()
        st.success(f" Muestra registrada con código: **{codigo}**")

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
            usuarios = cargar_usuarios()

            usuario_encontrado = next((u for u in usuarios if u["usuario"] == usuario_input), None)

            if usuario_encontrado:
                hash_guardado = usuario_encontrado["contrasena"]
                # Verificación segura de contraseña
                if bcrypt.checkpw(contraseña_input.encode(), hash_guardado.encode()):
                    st.session_state.logueado = True
                    st.session_state.usuario = usuario_input
                    st.session_state.rol = usuario_encontrado.get("rol", "superusuario")  # Guardar rol
                    st.success(f"Bienvenido, {usuario_input} ({st.session_state.rol})")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no encontrado.")

        st.markdown(
            """
            <div style="text-align: center; margin-top: 5px;">
                <a href="/registro" target="_blank" style="
                    background-color: #0057A0;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    display: inline-block;
                ">
                    Regístrate
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------
# -------------------------
# Flujo principal
# -------------------------
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "data" not in st.session_state:
    st.session_state.data = []
if not st.session_state.logueado:
    mostrar_login_con_imagen()
else:
    mostrar_header_doble()

    if st.button("🔒 Cerrar sesión"):
        cerrar_sesion()

    # Contenedor de bienvenida estilizado
    with st.container():
        st.markdown("""
            <div style='
                background-color: #f8f9fa;
                padding: 30px;
                border-radius: 12px;
                border: 1px solid #ddd;
                text-align: center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            '>
                <h2 style='color: #005B8F; font-family: "Segoe UI", sans-serif;'> Trazabilidad a Muestras de Agua</h2>
                <p style='font-size: 16px; color: #333;'>Utiliza las opciones a continuación para registrar o analizar muestras.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

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
        formulario_registro_muestra()
    
    elif st.session_state.pantalla == "recepcion":
        formulario_recepcion_muestra()

    elif st.session_state.pantalla == "analisis":
        formulario_analisis_laboratorio()

    elif st.session_state.pantalla == "informacion":
        formulario_informacion()

    elif st.session_state.pantalla == "usuarios":
        formulario_gestion_usuarios()





# FOOTER FINAL CON LOGO
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 15px; margin-top: 40px; background-color: #f2f2f2; border-radius: 8px;
                font-family: Arial, sans-serif; font-size: 14px;">
        <div style="flex: 2;">
            <b>Laboratorio de Calidad del Agua</b><br>
            Universidad Santo Tomás – Facultad de Ingeniería Ambiental<br>
            📍 Bogotá D.C. | ☎️ +57 314 367 9332<br>
            ✉️ km@usantotomas.edu.co
        </div>
        <div style="flex: 1; text-align: right;">
            <img src="data:image/png;base64,{logo_floter}" width="100">
        </div>
    </div>
""", unsafe_allow_html=True)

