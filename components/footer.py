import streamlit as st

from utils.style_loader import load_css
from utils.image_loader import image_to_base64

def render_footer():

    load_css("footer.css")
    logo_floter = image_to_base64("images/logo_floter.png") 
    
    st.markdown(
f"""
<div class="footer">
    <div class="footer-left">
        <b>Laboratorio de Calidad del Agua</b><br>
        Universidad Santo Tomás – Facultad de Ingeniería Ambiental<br>
        📍 Bogotá D.C. | ☎️ +57 314 367 9332<br>
        ✉️ km@usantotomas.edu.co
    </div>
    <div class="footer-right">
        <img src="data:image/png;base64,{logo_floter}" width="100">
    </div>
</div>
""",
        unsafe_allow_html=True
    )
