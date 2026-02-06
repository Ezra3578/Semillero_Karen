import json
import os
import streamlit as st

DATA_FILE = "data/muestras.json"


def load_samples():
    if "data" not in st.session_state:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state.data = json.load(f)
        else:
            st.session_state.data = []
    return st.session_state.data


def save_samples(samples: list[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=4, ensure_ascii=False)
