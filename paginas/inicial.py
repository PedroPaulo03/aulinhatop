import streamlit as st
import numpy as np
from google import genai
from google.genai import types

if not st.user.is_logged_in:
    st.title("FotoLateX")
    st.markdown("*Bem-vindo ao seu escrivão especializado! Aqui você pode acompanhar seus códigos em LateX.*")
    st.image('paginas/arquivos/imagelatex.png', width=200, use_container_width=True)
    st.markdown("Faça login com sua conta Google para o uso da ferramenta. ")
    # st.write(st.user)
    if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
            # Registra o usuário no Firestore se for o primeiro acesso (login_usuario faz isso)
            # REMOVIDO DAQUI: login_usuario() 
            st.login() # Função de login do Streamlit (redireciona)
            
    # Carrega conteúdo dos Termos para o Popover
        termos_content = "Não foi possível carregar os Termos de Uso e Política de Privacidade."
        try:
            termos_path = os.path.join(os.path.dirname(__file__), 'termos_e_privacidade.md')
            with open(termos_path, 'r', encoding='utf-8') as file:
                termos_content = file.read()
        except Exception as e:
            print(f"Erro ao carregar termos em app.py: {e}") # Log do erro
            # Mantém a mensagem padrão de erro
            
        # Popover com os termos carregados
        with st.popover("Ao fazer login, você concorda com nossos Termos de Uso e Política de Privacidade", use_container_width=True):
            st.markdown(termos_content, unsafe_allow_html=True)
                    
if st.sidebar.button("Log out"):
            st.logout()