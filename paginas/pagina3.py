    import streamlit as st
    from datetime import datetime
    import base64 # <-- **ADICIONAR ESTA LINHA** para decodificar a imagem

    from funcoes import (
        conectar_firebase
    )

    st.title("Visualize o Histórico de Códigos Feitos!")

    # Verifica se o usuário está autenticado
    if st.user: # Supondo que 'st.user' contém o objeto do usuário autenticado com o email
        db = conectar_firebase()
        colecao = 'usuarios2'
        referencia = db.collection(colecao).document(st.user.email).collection('saidas')

        saidas = list(referencia.stream())
        if saidas: # Se houver saídas para o usuário
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
                    # É bom logar ou exibir este erro para depuração
                    st.error(f'Erro ao transformar a data em formato legível para o ID {id}: {e}')
                
            visualizacao = st.selectbox(
                'Selecione uma saída para visualizar',
                options=lista_ids_saidas if lista_ids_saidas else ["Nenhuma saída disponível"]
            )

            if visualizacao != "Nenhuma saída disponível":
                # Em vez de usar index(), use dict para mapear o id legível para o id real do documento
                mapa_saidas = dict(zip(lista_ids_saidas, lista_docs_ids))
                doc_id_real = mapa_saidas[visualizacao]

                if st.button('Visualizar'):
                    # Cria **3 COLUNAS** para acomodar a imagem, LaTeX e Markdown
                    col1, col2, col3 = st.columns(3) # <-- **ALTERAÇÃO AQUI: DE 2 PARA 3 COLUNAS**

                    documento = (
                        db.collection(colecao)
                        .document(st.user.email)
                        .collection('saidas')
                        .document(doc_id_real)
                        .get()
                        .to_dict()
                    )

                    with col1: # <-- **NOVA COLUNA PARA A IMAGEM**
                        st.header('Imagem Original')
                        imagem_base64 = documento.get("imagem") # Tenta pegar a imagem em base64
                        if imagem_base64:
                            try:
                                # Decodifica a string base64 de volta para bytes
                                imagem_bytes_decoded = base64.b64decode(imagem_base64)
                                st.image(imagem_bytes_decoded, caption='Imagem Upada')
                            except Exception as e:
                                st.error(f"Erro ao decodificar a imagem: {e}")
                        else:
                            st.info("Nenhuma imagem encontrada para este registro.")

                    with col2: # <-- Coluna para LaTeX (agora a segunda)
                        st.header('Código LaTeX')
                        codigo_latex = documento.get("saida_latex", "Não encontrado")
                        st.code(codigo_latex, language='latex') # Adicionado 'language' para melhor destaque

                    with col3: # <-- Coluna para Markdown (agora a terceira)
                        st.header('Código Markdown')
                        codigo_markdown = documento.get("saida_markdown", "Não encontrado")
                        st.code(codigo_markdown, language='markdown') # Adicionado 'language' para melhor destaque
        else: # Caso o usuário logado não tenha nenhuma saída ainda
            st.info('Você ainda não carregou nenhuma imagem ou não há histórico disponível.')
    else: # Caso o usuário não esteja logado
        st.warning('Por favor, faça login para visualizar seu histórico.')

