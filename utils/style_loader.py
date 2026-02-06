import streamlit as st
from pathlib import Path

def load_css(filename: str):
    css_path = Path("styles") / filename

    if not css_path.exists():
        st.error(f"No se encontró el CSS: {filename}")
        return

    with open(css_path, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
