import streamlit as st

def hide_st_menu():
    st.markdown("""
        <style>
            /* Ocultar sidebar completo */
            [data-testid="stSidebar"] {
                display: none !important;
            }

            /* Ocultar navegación de páginas */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            /* Ocultar botón hamburguesa */
            [data-testid="collapsedControl"] {
                display: none !important;
            }

            /* Expandir contenido */
            [data-testid="stAppViewContainer"] > .main {
                margin-left: 0rem;
            }
        </style>
    """, unsafe_allow_html=True)
