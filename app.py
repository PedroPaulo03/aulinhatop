import streamlit as st 

paginas = {
    "Páginas": [ st.Page("paginas/inicial.py", title="Início", icon='💬', default=True),
                 st.Page("paginas/pagina1.py", title="Transformação", icon='✍️'),
                 st.Page("paginas/pagina2.py", title="Minha Conta", icon='👨‍💻'), 
                 st.Page("paginas/pagina3.py", title="Termos de Uso", icon='📄')
                 ]
    
}
# Usa a estrutura de páginas final (com ou sem Admin)
pg = st.navigation(paginas)
pg.run()