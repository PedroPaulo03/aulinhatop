import streamlit as st
import numpy as np
from google import genai
from google.genai import types

if not st.user.is_logged_in:
    st.title("FotoLateX")
    st.markdown("*Bem-vindo ao seu escrivão especializado! Aqui você pode acompanhar seus códigos em LateX.*")
    st.markdown("É necessário log in para o uso da ferramenta, clique no botão a seguir. ")
    # st.write(st.user)
    if st.button("Log in"):
        st.login()

if st.sidebar.button("Log out"):
    st.logout()