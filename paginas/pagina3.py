import streamlit as st

from funcoes import (
    conectar_firebase
)

st.title("Visualize o Histórico de Códigos Feitos!")


if st.user:
    db = conectar_firebase()
    colecao = 'usuarios2'
    referencia = db.collection(colecao).document(st.user.email).collection('saidas')

    # Pega todos os documentos da subcoleção
    docs = list(referencia.stream())

    if docs:  # verifica se a lista de documentos não está vazia
        lista_ids_saidas = []
        for doc in docs:
            doc_id = doc.id
            try:
                # Converte string para datetime
                dt = datetime.strptime(doc_id, "%Y%m%d%H%M%S")
                # Formata para string legível
                legivel = dt.strftime("%d/%m/%Y %H:%M:%S")
                lista_ids_saidas.append(f'Feito em: {legivel}')
            except Exception as e:
                print(f'Erro ao transformar a data em formato legível: {e}')

        visualizacao_index = st.selectbox('Selecione uma saída para visualizar', options=range(len(lista_ids_saidas)),
                                          format_func=lambda i: lista_ids_saidas[i])

        if st.button('Visualizar'):
            doc_selecionado = docs[visualizacao_index].to_dict()
            col1, col2 = st.columns(2)
            with col1:
                st.header('Código LaTeX')
                codigo_latex = doc_selecionado.get("saida_latex")
                st.code(codigo_latex)
            with col2:
                st.header('Código Markdown')
                codigo_markdown = doc_selecionado.get("saida_markdown")
                st.code(codigo_markdown)
    else:
        st.info('Você ainda não carregou nenhuma imagem. Acesse a aba Transformação para converter sua primeira imagem em código LaTeX ou Markdown!')
else:
    st.info('Você ainda não fez o login!')


