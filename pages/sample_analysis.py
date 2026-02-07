import streamlit as st
from datetime import datetime

from services.session_service import require_login, can

from utils.hide_st_menu import hide_st_menu
from utils.style_loader import load_css

from components.header import render_header
from components.footer import render_footer

from laboratory.application.laboratory import Laboratory
from laboratory.domain.parameters import FQ_PARAMETERS, MICRO_PARAMETERS, UNIDADES


lab = Laboratory()


hide_st_menu()
require_login() #Proteccion de login

#Config
st.set_page_config(
    page_title="Análisis de muestra",
    layout="wide"
)

#Header
render_header()

#Evitar acceso sin permiso
if not can("analizar_muestra"):
    st.error("No tienes permisos para acceder a esta sección")
    st.stop()

#Estilo
load_css("laboratory_pages.css")

#Regresar a la landing page
if st.button("Volver"):
    st.switch_page("pages/landing.py")


# Título
st.markdown(
    '<div class="titulo-seccion">Análisis de Muestra</div>',
    unsafe_allow_html=True
)

# Tabs: Analisis Fisico-Quimico / Analisis Microbiologico
opcion_tipo_analisis = st.radio("Selecciona una opción", 
                                ["Análisis Físico-Químicos", "Análisis Microbiológicos"], 
                                horizontal=True
                       )

def formato_analisis(pendientes: dict[str, dict],
                     analizadas: dict[str, dict],
                     parametros: list[str],
                     unidades: dict[str, str],
                     tipe: str  # "FQ" | "Micro"
                    ):
    

    opcion = st.radio(
        "Selecciona una opción",
        ["Muestras por analizar", "Muestras analizadas"],
        horizontal=True
    )

    # TAB 1: MUESTRAS POR ANALIZAR
    if opcion == "Muestras por analizar":

        if not pendientes:
            st.info("No hay muestras pendientes de análisis.")
            return

        seleccionadas = st.multiselect(
            "Selecciona las muestras que quieres analizar",
            list(pendientes.keys())
        )

        if not seleccionadas:
            return

        # Encabezado
        cols = st.columns([2, 1] + [1 for _ in seleccionadas])
        cols[0].markdown("**Ensayo**")
        cols[1].markdown("**Unidades**")
        for i, cod in enumerate(seleccionadas):
            cols[i + 2].markdown(f"**{cod}**")

        # Parámetros
        for param in parametros:
            cols = st.columns([2, 1] + [1 for _ in seleccionadas])
            cols[0].write(param)
            cols[1].write(unidades.get(param, ""))

            for i, cod in enumerate(seleccionadas):
                muestra = pendientes[cod]
                habilitado = param in muestra["analizar"]

                if not habilitado:              #Si no está habilitado lo salta
                    cols[i + 2].text_input(
                        "",
                        value="N/A",
                        disabled=True,
                        key=f"{cod}_{param}_na"
                    )
                    continue

                # -------- FQ --------
                if tipe == "FQ":                        #Si es FQ solo necesita 1 valor por parámetro
                    valor = cols[i + 2].number_input(
                        "",
                        key=f"{cod}_{param}",
                        format="%.2f"
                    )
                    st.session_state \
                        .setdefault("resultados_tmp", {}) \
                        .setdefault(cod, {})[param] = valor

                # -------- MICRO --------
                else:                                   #Si es Micro, requiere 2 valores
                    e1 = cols[i + 2].number_input(
                        "E1",
                        key=f"{cod}_{param}_e1",
                        format="%.2f"
                    )
                    e2 = cols[i + 2].number_input(
                        "E2",
                        key=f"{cod}_{param}_e2",
                        format="%.2f"
                    )
                    st.session_state \
                        .setdefault("resultados_tmp", {}) \
                        .setdefault(cod, {})[param] = {
                            "ensayo_1": e1,
                            "ensayo_2": e2
                        }

        # Guardar por muestra
        cols = st.columns([2, 1] + [1 for _ in seleccionadas])
        for i, cod in enumerate(seleccionadas):
            if cols[i + 2].button(f"Guardar {cod}", key=f"save_{cod}"):
                
                #Resultados en variable temporal
                resultados = st.session_state.get("resultados_tmp", {}).get(cod, {})

                #Realizar el analisis / persistencia
                lab.analyze_sample(
                    codigo=cod,
                    fq=resultados if tipe == "FQ" else {},
                    micro=resultados if tipe == "Micro" else {}
                )

                st.success(f"Muestra {cod} analizada correctamente")
                st.session_state.get("resultados_tmp", {}).pop(cod, None)
                st.rerun()

    # TAB 2: MUESTRAS ANALIZADAS
    else:
        if not analizadas:
            st.info("No hay muestras analizadas.")
            return

        st.markdown("### Muestras analizadas")

        for cod, info in analizadas.items():
            with st.expander(f"Muestra {cod}"):

                nuevos_resultados = {}

                for param in info["analizar"]:

                    # -------- FQ --------
                    if tipe == "FQ":
                        valor = info["resultados"].get(param, 0.0)
                        nuevo = st.number_input(
                            param,
                            value=valor,
                            key=f"edit_{cod}_{param}"
                        )
                        nuevos_resultados[param] = nuevo

                    # -------- MICRO --------
                    else:
                        ensayos = info["resultados"].get(param, {
                            "ensayo_1": 0.0,
                            "ensayo_2": 0.0
                        })

                        e1 = st.number_input(
                            f"{param} - Ensayo 1",
                            value=ensayos["ensayo_1"],
                            key=f"edit_{cod}_{param}_e1"
                        )
                        e2 = st.number_input(
                            f"{param} - Ensayo 2",
                            value=ensayos["ensayo_2"],
                            key=f"edit_{cod}_{param}_e2"
                        )

                        nuevos_resultados[param] = {
                            "ensayo_1": e1,
                            "ensayo_2": e2
                        }

                if st.button(f"Guardar cambios {cod}"):
                    lab.analyze_sample(
                        codigo=cod,
                        fq=nuevos_resultados if tipe == "FQ" else {},
                        micro=nuevos_resultados if tipe == "Micro" else {}
                    )
                    st.success(f"Resultados de {cod} actualizados")
                    st.rerun()



#PRUEBAS FISICO-QUIMICAS
if opcion_tipo_analisis == "Análisis Físico-Químicos":
    
    st.markdown(
        "<div class='section-title'>Análisis Físico-Químico</div>",
        unsafe_allow_html=True
    )

    pendientes = lab.get_analysis_view(tipe="FQ", state="pendiente")    #Encontrar las que están con pendiente
    analizadas = lab.get_analysis_view(tipe="FQ", state="analizado")    #Encontrar las que están con analizado

    formato_analisis(pendientes, analizadas, FQ_PARAMETERS, UNIDADES, "FQ")

#PRUEBAS MICROBIOLÓGICAS
elif opcion_tipo_analisis == "Análisis Microbiológicos":
    st.markdown(
        "<div class='section-title'>Análisis microbiológicos</div>",
        unsafe_allow_html=True
    )

    pendientes = lab.get_analysis_view(tipe="Micro", state="pendiente")    #Encontrar las que están con pendiente
    analizadas = lab.get_analysis_view(tipe="Micro", state="analizado")    #Encontrar las que están con analizado

    formato_analisis(pendientes, analizadas, MICRO_PARAMETERS, UNIDADES, "Micro")




render_footer()
