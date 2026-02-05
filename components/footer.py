import streamlit as st

def render_footer(logo_base64):
    st.markdown("""
    <style>
    .footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        margin-top: 40px;
        background-color: #f2f2f2;
        border-radius: 8px;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    .footer-left { flex: 2; }
    .footer-right { flex: 1; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="footer">
        <div class="footer-left">
            <b>Laboratorio de Calidad del Agua</b><br>
            Universidad Santo Tomás – Facultad de Ingeniería Ambiental<br>
            📍 Bogotá D.C. | ☎️ +57 314 367 9332<br>
            ✉️ km@usantotomas.edu.co
        </div>
        <div class="footer-right">
            <img src="data:image/png;base64,{logo_base64}" width="100">
        </div>
    </div>
    """, unsafe_allow_html=True)
