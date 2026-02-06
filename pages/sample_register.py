import streamlit as st

from services.session_service import require_login, can

from utils.hide_st_menu import hide_st_menu

from components.header import render_header
from components.footer import render_footer

from laboratory.application.laboratory import Laboratory

lab = Laboratory()


hide_st_menu()
require_login()

st.set_page_config(page_title="Registro de muestra", layout="wide")

render_header()

if not can("registrar_muestra"):
    st.error("No tienes permisos")
    st.stop()

st.markdown("""
    <div class='title'>
        <h1 style='color: #FFFFFF;'>Registro de Muestra</h1>
    </div>
""", unsafe_allow_html=True)

if st.button("Volver"):
    st.switch_page("pages/landing.py")


# INTERFAZ FORMULARIO
def formulario_registro_muestra():

    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 25px; border-radius: 10px; border: 1px solid #ccc;'>
            <h3 style='color: #0057A0;'>Registro de Muestra</h3>
        </div>
    """, unsafe_allow_html=True)

    # Interfaz
    col1, col2 = st.columns(2)

    with col1:
        tipo_muestra = st.selectbox(
            "Tipo de Muestra", ["", "Interna", "Red", "Externa"]
        )

        codigo_punto_red = None
        if tipo_muestra == "Red":
            opciones = st.session_state.setdefault(
                "puntos_red",
                ["San Cristóbal", "Silveria Espinoza", "Santa Rita", "Copihue", "Alcaldía",
                 "Girardot", "Arboleda", "Manablanca", "Carcel de la policia", "Batallón",
                 "Universidad", "Coliseo", "Brasilia", "Hospital", "SENA", "Prado",
                 "Pueblo Viejo", "Villa Olímpica"]
            )

            seleccion = st.selectbox(
                "Código del punto de red",
                [""] + opciones + ["Crear nuevo punto de red"]
            )

            if seleccion == "Crear nuevo punto de red":
                nuevo = st.text_input("Ingrese el nuevo código del punto de red")
                if nuevo:
                    codigo_punto_red = nuevo
            elif seleccion:
                codigo_punto_red = seleccion

        fecha = st.date_input("Fecha")
        quien_muestrea = st.text_input("Persona que tomó la muestra")

        dispositivo = st.selectbox(
            "Dispositivo de Toma de Muestra",
            ["", "Manguera", "Canal", "Grifo", "Otro"]
        )
        if dispositivo == "Otro":
            dispositivo = st.text_input("Especifique el dispositivo")

        tipo_agua = st.selectbox(
            "Tipo de Agua",
            ["", "Agua potable (AP)", "Agua superficial (ASP)",
             "Agua subterránea (ASB)", "Agua envasada (AE)",
             "Agua lluvia (AL)", "Otra (O)"]
        )
        if tipo_agua == "Otra (O)":
            tipo_agua = st.text_input("Especifique el tipo de agua")

    with col2:
        hora = st.time_input("Hora", disabled=True)
        fuente = st.selectbox("Fuente de Abastecimiento", ["", "Andes Medio", "Mancilla Bajo", 
                                                           " Botello Alto", "San Rafael I", 
                                                           "San Rafael II", "Deudoro Aponte", 
                                                           "Manablanca","Cartagenita","Guapucha II",
                                                           "Gatillo 0","Gatillo 1", "Gatillo 2","Gatillo 3"])
        observaciones = st.text_area("Observaciones")

    
    st.markdown("""
        <div style='background-color: #f0f4f8; padding: 25px; border-radius: 10px; border: 1px solid #ccc;'>
               <h3 style='color: #0057A0;'>Datos In Situ</h3>
        </div>
    """, unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)
    ph = col3.number_input("pH", format="%.2f")
    cloro = col4.number_input("Cloro (mg/L)", format="%.2f")
    temperatura = col5.number_input("Temperatura (°C)", format="%.2f")

    # ---------- Acción ----------
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

formulario_registro_muestra()

render_footer()
