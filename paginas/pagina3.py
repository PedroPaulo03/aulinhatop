import streamlit as st

from funcoes import (
    conectar_firebase
)

st.title("Visualize o Histórico de Códigos Feitos!")


if st.user:
    db = conectar_firebase()
    colecao = 'usuarios2'
    referencia = db.collection(colecao).document(st.user.email).collection('saidas')

    saidas = list(referencia.stream())
    if saidas:
        lista_ids_saidas = []
        lista_docs_ids = []
        for doc in saidas:
            id = doc.id
            try:
                 # Converte string para datetime
                dt = datetime.strptime(id, "%Y%m%d%H%M%S")
                # Formata para string legível
                legivel = dt.strftime("%d/%m/%Y %H:%M:%S")
                lista_ids_saidas.append(f'Feito em: {legivel}')
                lista_docs_ids.append(id)

            except Exception as e:
                print(f'Erro ao transformar a data em formato legível: {e}')
            
        visualizacao = st.selectbox('Selecione uma saída para visualizar', options = lista_ids_saidas)
        idx = lista_ids_saidas.index(visualizacao)
        doc_id_real = lista_docs_ids[idx]

        if st.button('Visualizar'):
            col1, col2 = st.columns(2)
            documento = db.collection(colecao).document(st.user.email).collection('saidas').document(doc_id_real).get().to_dict()
             
            with col1:
                 st.header('Código LaTeX')
                 codigo_latex = documento.get("saida_latex")
                 st.code(codigo_latex)
            with col2:
                 st.header('Código Markdown')
                 codigo_markdown = documento.get("saida_markdown")
                 st.code(codigo_markdown)
    else:
        st.info('Você ainda não carregou nenhuma imagem. Acesse a aba Transformação para converter sua primeira imagem em código LaTeX ou Markdown!')
else:
    st.info('Você ainda não fez o login!')


