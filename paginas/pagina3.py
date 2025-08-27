import streamlit as st

from funcoes import (
    conectar_firebase
)

st.title("Visualize o Histórico de Códigos Feitos!")


if st.user:
    db = conectar_firebase()
    colecao = 'usuarios2'
    referencia = db.colletion(colecao).document(st.user.email).collection('saidas')

    if saidas:
        docs = referencia.stream()
        lista_ids_saidas = []
        for doc in docs:
            id = doc.id
            try:
                 # Converte string para datetime
                dt = datetime(id, "%Y%m%d%H%M%S")
                # Formata para string legível
                legivel = dt.strftime("%d/%m/%Y %H:%M:%S")
                lista_ids_saidas.append(f'Feito em: {legivel}')

            except Exception as e:
                return f'Erro ao transformar a data em formato legível: {e}'
            
        visualizacao = st.selectbox('Selecione uma saída para visualizar', options = lista_ids_saidas)

        if st.button('Visualizar'):
            
    else:
        st.info('Você ainda não carregou nenhuma imagem. Acesse a aba Transformação para converter sua primeira imagem em código LaTeX ou Markdown!')
else:
    st.info('Você ainda não fez o login!')


