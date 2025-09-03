import streamlit as st
from datetime import datetime
import base64 # Esta linha também na coluna zero

# Esta linha também na coluna zero
from funcoes import (
    conectar_firebase
    )

# Esta linha também na coluna zero
st.title("Visualize o Histórico de Códigos Feitos!")


# Tudo dentro deste 'if' deve estar indentado uma vez
if st.user: 
    # Tudo dentro deste 'if' deve estar indentado uma vez
    db = conectar_firebase()
    colecao = 'usuarios2'
    referencia = db.collection(colecao).document(st.user.email).collection('saidas')

    saidas = list(referencia.stream())
    # Tudo dentro deste 'if' deve estar indentado duas vezes
    if saidas: 
        lista_ids_saidas = []
        lista_docs_ids = []
        # Tudo dentro deste 'for' deve estar indentado três vezes
        for doc in saidas:
            id = doc.id
            # Tudo dentro deste 'try' deve estar indentado quatro vezes
            try:
                # Converte string para datetime
                dt = datetime.strptime(id, "%Y%m%d%H%M%S")

                # Formata para string legível
                legivel = dt.strftime("%d/%m/%Y %H:%M:%S")
                lista_ids_saidas.append(f'Feito em: {legivel}')
                lista_docs_ids.append(id)

            # Tudo dentro deste 'except' deve estar indentado quatro vezes
            except Exception as e:
                # É bom logar ou exibir este erro para depuração
                st.error(f'Erro ao transformar a data em formato legível para o ID {id}: {e}')
            
        # Esta linha deve estar indentada duas vezes (fora do for)
        visualizacao = st.selectbox(
            'Selecione uma saída para visualizar',
            options=lista_ids_saidas if lista_ids_saidas else ["Nenhuma saída disponível"]
        )

        # Tudo dentro deste 'if' deve estar indentado duas vezes
        if visualizacao != "Nenhuma saída disponível":
            # Tudo dentro deste 'if' deve estar indentado três vezes
            # Em vez de usar index(), use dict para mapear o id legível para o id real do documento
            mapa_saidas = dict(zip(lista_ids_saidas, lista_docs_ids))
            doc_id_real = mapa_saidas[visualizacao]

            # Tudo dentro deste 'if' deve estar indentado três vezes
            if st.button('Visualizar'):
                # Cria **3 COLUNAS** para acomodar a imagem, LaTeX e Markdown
                # Indentado quatro vezes
                col1, col2, col3 = st.columns(3) 

                # Indentado quatro vezes
                documento = (
                    db.collection(colecao)
                    .document(st.user.email)
                    .collection('saidas')
                    .document(doc_id_real)
                    .get()
                    .to_dict()
                )

                # Indentado quatro vezes
                with col1: # Nova coluna para a imagem
                    # Tudo dentro deste 'with' deve estar indentado cinco vezes
                    st.header('Imagem Original')
                    imagem_base64 = documento.get("imagem") # Tenta pegar a imagem em base64
                    # Tudo dentro deste 'if' deve estar indentado seis vezes
                    if imagem_base64:
                        # Tudo dentro deste 'try' deve estar indentado sete vezes
                        try:
                            # Decodifica a string base64 de volta para bytes
                            imagem_bytes_decoded = base64.b64decode(imagem_base64)
                            st.image(imagem_bytes_decoded, caption='Imagem Upada')
                        # Tudo dentro deste 'except' deve estar indentado sete vezes
                        except Exception as e:
                            st.error(f"Erro ao decodificar a imagem: {e}")
                    # Tudo dentro deste 'else' deve estar indentado seis vezes
                    else:
                        st.info("Nenhuma imagem encontrada para este registro.")

                # Indentado quatro vezes
                with col2: # Coluna para LaTeX (agora a segunda)
                    # Tudo dentro deste 'with' deve estar indentado cinco vezes
                    st.header('Código LaTeX')
                    codigo_latex = documento.get("saida_latex", "Não encontrado")
                    st.code(codigo_latex, language='latex') # Adicionado 'language' para melhor destaque

                # Indentado quatro vezes
                with col3: # Coluna para Markdown (agora a terceira)
                    # Tudo dentro deste 'with' deve estar indentado cinco vezes
                    st.header('Código Markdown')
                    codigo_markdown = documento.get("saida_markdown", "Não encontrado")
                    st.code(codigo_markdown, language='markdown') # Adicionado 'language' para melhor destaque
    # Tudo dentro deste 'else' (do if saidas:) deve estar indentado uma vez
    else: # Caso o usuário logado não tenha nenhuma saída ainda
        st.info('Você ainda não carregou nenhuma imagem ou não há histórico disponível.')
# Tudo dentro deste 'else' (do if st.user:) deve estar indentado uma vez
else: # Caso o usuário não esteja logado
    st.warning('Por favor, faça login para visualizar seu histórico.')

else:
    st.warning("Você precisa estar logado para usar esta funcionalidade.")

if st.sidebar.button("Log out"):
    st.logout()