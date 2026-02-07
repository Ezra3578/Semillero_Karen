import streamlit as st
import pandas as pd

from laboratory.application.laboratory import Laboratory
from laboratory.domain.parameters import MESES

from services.session_service import require_login, can
from services.excel.excel_generator import Excel
from services.pdf.pdf_generator import PDF

from utils.hide_st_menu import hide_st_menu
from utils.style_loader import load_css

from components.header import render_header
from components.footer import render_footer

lab = Laboratory()

#Ocultar menús de Streamlit
hide_st_menu()

require_login()#Protección de login

#Configuracion básica de la page
st.set_page_config(page_title="Información de Muestras", layout="wide")

#Header
render_header()

# Verificar permisos
if not can("ver_informacion_muestra"):
    st.error("No tienes permisos para acceder a esta sección")
    st.stop()

# Cargar CSS
load_css("laboratory_pages.css")

# Volver a landing
if st.button("Volver"):
    st.switch_page("pages/landing.py")

#Titulo
st.markdown("<div class='titulo-seccion'>Información de Muestras</div>", unsafe_allow_html=True)

#Obtener todas las muestras
samples = lab.get_samples()

#Filtro de Fuente
fuente_filtro = st.selectbox("Fuente de abastecimiento", [""] + sorted(set(m["Fuente"] for m in samples)))

#Filtro de mes
meses_disponibles = sorted(set(m["Código"][3:5] for m in samples))  # Obtener los meses disponibles en las muestras
meses_nombres = [MESES[m] for m in meses_disponibles]               # Convertir a nombres
mes_seleccionado_nombre = st.selectbox("Mes", [""] + meses_nombres) # Selectbox mostrando nombres

# Convertir de vuelta a código de mes para filtrar
mes_seleccionado = None
if mes_seleccionado_nombre: 
    mes_seleccionado = next(k for k, v in MESES.items() if v == mes_seleccionado_nombre)    # Buscar la clave del dict que corresponde al nombre seleccionado

#Filtro de día
dia_filtro = st.selectbox("Día (DD)", [""] + sorted(set(m["Código"][5:7] for m in samples)))

# Aplicar filtros
filtradas = samples
if fuente_filtro:
    filtradas = [m for m in filtradas if m["Fuente"] == fuente_filtro]
if mes_seleccionado:
    filtradas = [m for m in filtradas if m["Código"][3:5] == mes_seleccionado]
if dia_filtro:
    filtradas = [m for m in filtradas if m["Código"][5:7] == dia_filtro]

#Selección de muestras
seleccionadas_codigos = st.multiselect(
    "Selecciona las muestras que quieres visualizar/exportar (Agregar un filtro previo borrará la selección actual)",
    options=[m["Código"] for m in filtradas],
)

seleccionadas = [m for m in filtradas if m["Código"] in seleccionadas_codigos]

# MOSTRAR TABLA
if seleccionadas:
    df = pd.DataFrame(seleccionadas)
    # Convertir resultados a strings para mostrar
    df["FQ"] = df["Resultados"].apply(lambda d: "\n".join([f"{k}: {v}" for k, v in d.get("FQ", {}).items()]))
    df["Micro"] = df["Resultados"].apply(
        lambda d: "\n".join(
        [
            f"{k}: {((v.get('ensayo_1', 0) + v.get('ensayo_2', 0)) / 2):.2f}"   #Del segundo parámetro obtiene cada ensayo y los promedia
            for k, v in d.get("Micro", {}).items()  #Busca los items de Micro en Resultados
        ]
        )
    )
    df = df.drop(columns=["Resultados"], errors="ignore")
    
    st.dataframe(df, use_container_width=True)

    # ---------- DESCARGAS ----------
    st.download_button(
        "Descargar Excel",
        Excel.generar_excel_estilo_laboratorio(seleccionadas),
        file_name="Resultados_Muestras.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        "Descargar PDF",
        PDF.generar_pdf_masivo(data=seleccionadas),
        file_name="Resultados_Muestras.pdf",
        mime="application/pdf"
    )
else:
    st.info("Aplica filtros y selecciona al menos una muestra para visualizar/exportar.")

render_footer()