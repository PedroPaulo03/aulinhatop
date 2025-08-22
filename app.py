import streamlit as st
import numpy as np
from google import genai
from google.genai import types


paginas_privadas = [
    st.Page("paginas/pagina1.py", title="Transformação", icon='✍️', default = True),
    st.Page("paginas/pagina2.py", title="Minha Conta", icon='👨‍💻')
]

if st.user.is_logged_in:
    paginas = {
        "Páginas": paginas_privadas
    }

    pg = st.navigation(paginas)
    pg.run()
         with st.sidebar:
             st.logout()

else:
    st.title("FotoLateX")
    st.markdown("*Bem-vindo ao seu escrivão especializado! Aqui você pode acompanhar seus códigos em LateX.*")
    st.image('paginas/arquivos/imagelatex.png', width=200, use_container_width=True)
    st.markdown("Faça login com sua conta Google para o uso da ferramenta. ")
    # st.write(st.user)
    if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
        st.login() # Função de login do Streamlit (redireciona)

    with open('termos_e_privacidade.md', 'r', encoding='utf-8') as file:
        termos_content = file.read()

    with st.popover("Ao fazer login, você concorda com nossos Termos de Uso e Política de Privacidade", use_container_width=True):
        st.markdown(termos_content, unsafe_allow_html=True)

