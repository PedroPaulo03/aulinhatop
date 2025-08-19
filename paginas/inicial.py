import streamlit as st
import numpy as np
from google import genai
from google.genai import types

if not st.user.is_logged_in:
    st.title("FotoLateX")
    st.markdown("*Bem-vindo ao seu escrivão especializado! Aqui você pode acompanhar seus códigos em LateX.*")
    st.markdown("É necessário log in para o uso da ferramenta, clique no botão a seguir. ")
    # Logo centralizada
        st.image('arquivos/capa.jpg', width=200, use_container_width=True)
        # Botão de login
        if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
            # Registra o usuário no Firestore se for o primeiro acesso (login_usuario faz isso)
            # REMOVIDO DAQUI: login_usuario() 
            st.login() # Função de login do Streamlit (redireciona)
    # st.write(st.user)
    if st.button("Log in"):
        st.login()

if st.sidebar.button("Log out"):
    st.logout()