import streamlit as st
import numpy as np
from google import genai
from google.genai import types

if not st.user.is_logged_in:
    st.title("FotoLateX")
    st.markdown("*Bem-vindo ao seu escrivão especializado! Aqui você pode acompanhar seus códigos em LateX.*")
    st.image('paginas/arquivos/unnamed.jpg', width=200, use_container_width=True)
    st.markdown("Faça login com sua conta Google para o uso da ferramenta. ")
    # st.write(st.user)
    if st.button("Log in"):
        st.login()

if st.sidebar.button("Log out"):
    st.logout()