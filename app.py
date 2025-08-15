import streamlit as st 

paginas = {
    "Página de acesso": [ st.Page("pagina/inicial.py", title="Início", default=True)],
    
    "Transformações": [ st.Page("paginas/pagina1.py", title="Escrivão LaTeX"), 
           ]
}

# Usa a estrutura de páginas final (com ou sem Admin)
pg = st.navigation(paginas)
pg.run()


