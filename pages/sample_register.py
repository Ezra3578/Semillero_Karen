import streamlit as st

from services.session_service import require_login, can

from utils.hide_st_menu import hide_st_menu
from utils.style_loader import load_css

from components.header import render_header
from components.footer import render_footer

from laboratory.application.laboratory import Laboratory
from laboratory.domain.parameters import TIPOS_MUESTRA, PUNTOS_RED, DISPOSITIVOS_TOMA, TIPOS_AGUA, FUENTES_ABASTECIMIENTO

lab = Laboratory()

#Ocultar menu de Streamlit
hide_st_menu()

#Evitar acceso sin login
require_login()

#Configuracion de pagina
st.set_page_config(page_title="Registro de muestra", layout="wide")

#Header
render_header()

#Evitar acceso sin permiso de rol
if not can("registrar_muestra"):
    st.error("No tienes permisos")
    st.stop()

load_css("laboratory_pages.css")

#Volver a la landing page
if st.button("Volver"):
    st.switch_page("pages/landing.py")


# Título
st.markdown(
    '<div class="titulo-seccion">Registro de muestra</div>',
    unsafe_allow_html=True
)

# Interfaz
col1, col2 = st.columns(2)

with col1:
    #Tipo de muestra
    tipo_muestra = st.selectbox(
        "Tipo de Muestra", 
        TIPOS_MUESTRA
    )

    codigo_punto_red = None
    
    #Campo opcional de Red
    if tipo_muestra == "Red":
        
        #Puntos de red por defecto
        opciones = st.session_state.setdefault(
            "puntos_red",
            PUNTOS_RED
        )

        seleccion = st.selectbox(
            "Código del punto de red",
            [""] + opciones + ["Crear nuevo punto de red"]
        )

        #Agregar un nuevo punto de red
        if seleccion == "Crear nuevo punto de red":
            nuevo = st.text_input("Ingrese el nuevo código del punto de red")
            if nuevo:
                codigo_punto_red = nuevo
        elif seleccion:
            codigo_punto_red = seleccion

    #Fecha
    fecha = st.date_input("Fecha")
    
    #Quien_muestrea
    quien_muestrea = st.text_input("Persona que tomó la muestra")

    #Dispositivo de toma de muestra
    dispositivo = st.selectbox(
        "Dispositivo de Toma de Muestra",
        DISPOSITIVOS_TOMA
    )

    #Agregar nuevo dispositivo
    if dispositivo == "Otro":
        dispositivo = st.text_input("Especifique el dispositivo")

    #Tipos de agua
    tipo_agua = st.selectbox(
        "Tipo de Agua",
        TIPOS_AGUA
    )

    #Agregar tipo de agua
    if tipo_agua == "Otra (O)":
        tipo_agua = st.text_input("Especifique el tipo de agua")

with col2:

    #Hora de Registro
    hora = st.time_input("Hora", step=60)

    #Fuente de abastecimiento
    fuente = st.selectbox(
        "Fuente de Abastecimiento",
        FUENTES_ABASTECIMIENTO    
    )
    observaciones = st.text_area("Observaciones")

#Titulo
st.markdown(
    '<div class="titulo-seccion">Datos in Situ</div>',
    unsafe_allow_html=True
)

col3, col4, col5 = st.columns(3)

#Registrar ph
ph = col3.number_input("pH", format="%.2f")

#Registrar cloro
cloro = col4.number_input("Cloro (mg/L)", format="%.2f")

#Registrar Temperatura
temperatura = col5.number_input("Temperatura (°C)", format="%.2f")

#Guardar
if st.button("Guardar muestra", use_container_width=True):
    data = {
        "tipo_muestra": tipo_muestra,
        "fecha": fecha,
        "hora": hora,
        "quien_muestra": quien_muestrea,
        "dispositivo": dispositivo,
        "tipo_agua": tipo_agua,
        "fuente": fuente,
        "codigo_red": codigo_punto_red,  # None si no aplica
        "ph": ph,
        "cloro": cloro,
        "temperatura": temperatura,
        "observaciones": observaciones,
    }

    try:
        sample = lab.register_sample(data)
        
        st.success(f"Muestra registrada: **{sample.codigo}**")
    except ValueError as e:
        st.warning(str(e))

render_footer()