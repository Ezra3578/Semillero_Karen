import streamlit as st
from datetime import datetime

from services.session_service import require_login, can

from utils.hide_st_menu import hide_st_menu
from utils.style_loader import load_css

from components.header import render_header
from components.footer import render_footer

from laboratory.application.laboratory import Laboratory
from laboratory.domain.parameters import FQ_PARAMETERS, MICRO_PARAMETERS


lab = Laboratory()


hide_st_menu()
require_login() #Proteccion de login

#Config
st.set_page_config(
    page_title="Recepción de muestra",
    layout="wide"
)

#Header
render_header()

#Evitar acceso sin permiso
if not can("recibir_muestra"):
    st.error("No tienes permisos para acceder a esta sección")
    st.stop()

#Estilo
load_css("laboratory_pages.css")


#Estado de la pestaña de recepcion
if "tab_recepcion" not in st.session_state:
    st.session_state.tab_recepcion = "nuevas"

#Regresar a la landing page
if st.button("Volver"):
    st.switch_page("pages/landing.py")

# Título
st.markdown(
    '<div class="titulo-seccion">Recepción de muestra</div>',
    unsafe_allow_html=True
)


# Navegación
col1, col2 = st.columns(2)

with col1:
    if st.button("Recepción de muestra", use_container_width=True):
        st.session_state.tab_recepcion = "nuevas"

with col2:
    if st.button("Muestras recepcionadas", use_container_width=True):
        st.session_state.tab_recepcion = "recepcionadas"


# TAB 1: Nuevas recepciones
if st.session_state.tab_recepcion == "nuevas":

    pendientes = lab.get_pending_samples()

    if not pendientes:
        st.info("No hay muestras pendientes de recepción.")

    else:
        codigo = st.selectbox(
            "Seleccione la muestra registrada",
            [s["Código"] for s in pendientes]
        )

        col_a, col_b = st.columns(2)

        with col_a:
            fecha_recepcion = st.date_input(
                "Fecha de recepción",
                value=datetime.today()
            )
            temperatura_recepcion = st.number_input(
                "Temperatura de recepción (°C)",
                format="%.2f"
            )

        with col_b:
            hora_recepcion = st.time_input("Hora de recepción")
            recepciona = st.text_input("Recepciona")

        st.markdown("---")

        seleccion_fq = st.multiselect(
            "Parámetros físico-químicos",
            FQ_PARAMETERS
        )

        seleccion_micro = st.multiselect(
            "Parámetros microbiológicos",
            MICRO_PARAMETERS
        )

        if st.button("Guardar recepción", use_container_width=True):
            try:
                lab.receive_sample(
                    codigo=codigo,
                    fecha_recepcion=fecha_recepcion,
                    hora_recepcion=hora_recepcion,
                    temperatura_recepcion=temperatura_recepcion,
                    recepciona=recepciona,
                    parametros_fq=seleccion_fq,
                    parametros_micro=seleccion_micro,
                )

                st.success(f"Muestra {codigo} recepcionada correctamente")
                st.rerun()

            except ValueError as e:
                st.warning(str(e))

# TAB 2: Muestras recepcionadas
elif st.session_state.tab_recepcion == "recepcionadas":

    #Filtra por "recibida"
    recepcionadas = lab.get_received_samples()

    #Si no hay
    if not recepcionadas:
        st.info("No hay muestras recepcionadas.")

    else:
        for muestra in recepcionadas:
            with st.expander(f"Muestra {muestra['Código']}"):
                
                #QUIÉN RECEPCIONÓ
                st.write(f"Recepcionó: **{muestra.get('Recepcionó', '')}**")

                #PARAMETROS DESDE EL JSON
                fq_guardados = (
                    muestra.get("Parámetros a analizar", {}).get("FQ", [])
                )
                micro_guardados = (
                    muestra.get("Parámetros a analizar", {}).get("Micro", [])
                )

                #NUEVA SELECCION
                seleccion_fq = st.multiselect(
                    "Parámetros físico-químicos",
                    FQ_PARAMETERS,
                    default=fq_guardados,
                    key=f"fq_{muestra['Código']}"
                )

                seleccion_micro = st.multiselect(
                    "Parámetros microbiológicos",
                    MICRO_PARAMETERS,
                    default=micro_guardados,
                    key=f"micro_{muestra['Código']}"
                )

                if st.button(f"Guardar cambios {muestra['Código']}", use_container_width=True):
                    try:
                        lab.update_reception_parameters(
                            codigo=muestra["Código"],
                            parametros_fq=seleccion_fq,
                            parametros_micro=seleccion_micro,
                        )

                        st.success("Parámetros actualizados correctamente")
                        st.rerun()

                    except ValueError as e:
                        st.warning(str(e))

render_footer()
