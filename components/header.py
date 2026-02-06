import streamlit as st
import streamlit.components.v1 as components

from utils.image_loader import image_to_base64

def render_header():

    logo_usta = image_to_base64("images/LOGO USTA.png")
    logo_empresa = image_to_base64("images/LOGO.png")
    logo_nombre = image_to_base64("images/NOMBRE LOGO.png")

    st.markdown(f"""
        <!-- Franja superior gris -->
        <div style="background-color: #e5e5e5; padding: 5px 30px; display: flex; align-items: center; justify-content: flex-end; border-radius: 18px 18px 0px 0px;">
            <img src="data:image/png;base64,{logo_usta}" style="height: 60px;">
        </div>

        <!-- Franja inferior con logos de empresa y texto -->
        <div style="background-color: white; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between;  border-radius: 0px 0px 18px 18px;">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="data:image/png;base64,{logo_empresa}" style="height: 70px;">
                <div style="border-left: 2px solid #ccc; height: 60px;"></div>
                <img src="data:image/png;base64,{logo_nombre}" style="height: 70px;">
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="border-left: 2px solid #ccc; height: 60px;"></div>
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100%;
                    padding-left: 20px;
                ">
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        color: #0057A0;
                        font-family: 'Segoe UI Semibold', 'Segoe UI', sans-serif;
                        letter-spacing: 1.2px;
                        line-height: 1.1;
                        text-align: center;
                    ">
                        Sistema de registro de<br>muestras
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)