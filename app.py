import streamlit as st

paginas_publicas = [
    st.Page("paginas/inicial.py", title="Início", icon='💬', default=True),
    st.Page("paginas/pagina3.py", title="Termos de Uso", icon='📄')
]

paginas_privadas = [
    st.Page("paginas/pagina1.py", title="Transformação", icon='✍️'),
    st.Page("paginas/pagina2.py", title="Minha Conta", icon='👨‍💻')
]

if st.user.is_logged_in:
    paginas = {
        "Páginas": paginas_publicas + paginas_privadas
    }
else:
    paginas = {
        "Páginas": paginas_publicas
    }

pg = st.navigation(paginas)
pg.run()