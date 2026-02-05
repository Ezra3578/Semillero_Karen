import streamlit as st
from pathlib import Path

def load_css(filename: str):
    css_path = Path("styles") / filename
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )