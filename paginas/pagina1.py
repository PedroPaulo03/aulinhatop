import streamlit as st
import numpy as np
from funcoes import(
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,
    gerar_estruturado,
    salvar_saidas # <--- ADIÇÃO: Importa a função para salvar no Firebase
)
from typing import List

st.set_page_config(layout = "wide")

st.title("✍️ Transforme seus textos escritos em formato LaTeX")
st.info("Instruções: Este app foi pensando para atenter as seguintes pessoas: o monitor, professor, aluno e pesquisador que ao fazer algo de maneira escrita na mão grande no papel, quadro ou tablet, que contenha fórmulas matemáticas dutante o texto e tem interesse em digitalizar o arquivo, passando assim para o formato LateX, e é nessa prte que entramos, preparamos a escrita no LateX para você.")


imagens_carregadas = st.file_uploader(
    "Selecione uma imagem (.png, .jpeg, .jpg) )",
    type=["png", "jpeg", "jpg"],
    accept_multiple_files=True
)

if imagens_carregadas is None or len(imagens_carregadas) == 0:
    st.info("Por favor, carregue uma imagem para começar.")

col1, col2 = st.columns(2)

# Variável para armazenar os bytes da imagem visualizada no preview
imagem_bytes_para_preview = None # <--- ADIÇÃO: Inicializa a variável

with col1:
    # <--- CORREÇÃO AQUI: A condição 'imagens_carregadas is True' está incorreta para listas.
    if imagens_carregadas: # Verifica se a lista de imagens carregadas não está vazia ou None
        st.subheader('Pré-visualização da imagem')
        imagem_visualizada = st.selectbox(label='Selecione a imagem para pré-visualização',
                                        format_func=lambda img: img.name if img else "Arquivo desconhecido",
                                        options = imagens_carregadas, index = 0, label_visibility='hidden')
        if imagem_visualizada is not None:
            imagem_bytes_para_preview = imagem_visualizada.getvalue() # Armazena os bytes da imagem selecionada para preview
            st.image(imagem_bytes_para_preview, caption="Imagem selecionada", use_container_width=True)
    # Não precisamos de um 'else' aqui, pois a imagem_visualizada já será None se não houver imagens.


# Variáveis para armazenar as saídas acumuladas de TODAS as imagens (para exibição e download)
saidas_latex_acumuladas = ''
saidas_markdown_acumuladas = ''

# <--- ADIÇÃO: Lista para armazenar os resultados de CADA imagem processada para salvar individualmente no Firebase
resultados_processados_para_salvar = []

with col2:
    if imagens_carregadas and len(imagens_carregadas) > 0:
        if st.button("Processar Imagem e Gerar Códigos", key="process_button", use_container_width=True):
            # Limpa as variáveis acumuladoras e a lista de resultados a cada novo processamento
            saidas_latex_acumuladas = ''
            saidas_markdown_acumuladas = ''
            resultados_processados_para_salvar = []

            for i, imagem_carregada_loop in enumerate(imagens_carregadas): # <--- MUDANÇA: Renomeado para clareza
                if imagem_carregada_loop.getvalue():
                    with st.spinner(f"Convertendo texto da página {i+1} para Markdown e LaTeX...", show_time=True):
                        file_bytes_processado = imagem_carregada_loop.getvalue() # <--- MUDANÇA: Obtém os bytes da imagem atual do loop
                        try:
                            # A função 'gerar_estruturado' já retorna LaTeX e Markdown estruturados
                            saida_markdown_unica, saida_latex_unica = gerar_estruturado(file_bytes_processado, type=imagem_carregada_loop.type)

                            # Acumula para exibição e download final
                            saidas_markdown_acumuladas += saida_markdown_unica + "\n\n"
                            saidas_latex_acumuladas += saida_latex_unica + "\n\n"

                            # <--- ADIÇÃO: Armazena os resultados de CADA imagem na lista para salvar no Firebase
                            resultados_processados_para_salvar.append({
                                'imagem_bytes': file_bytes_processado,
                                'saida_markdown': saida_markdown_unica,
                                'saida_latex': saida_latex_unica,
                                'markdown_estruturado': saida_markdown_unica, # 'gerar_estruturado' já produz o formato estruturado
                                'latex_estruturado': saida_latex_unica        # 'gerar_estruturado' já produz o formato estruturado
                            })

                        except Exception as e:
                            st.error(f"Erro ao processar a imagem '{imagem_carregada_loop.name}': {e}") # <--- MUDANÇA: Mensagem de erro mais específica
                else:
                    st.warning(f"Nenhum arquivo válido foi carregado para processamento na imagem '{imagem_carregada_loop.name}'.") # <--- MUDANÇA: Mensagem de aviso mais específica

            # Exibir o resultado em LaTeX (agora as saídas acumuladas)
            st.markdown("---")
            st.subheader("Visualização dos Códigos Gerados (todos):") # <--- MUDANÇA: Título para clareza
            st.markdown(saidas_markdown_acumuladas)

            # <--- ADIÇÃO: Bloco para salvar no Firebase após processar TODAS as imagens
            # Verifica se o usuário está logado e se há resultados para salvar
            if hasattr(st, 'user') and st.user and resultados_processados_para_salvar:
                with st.spinner("Salvando resultados no histórico do Firebase...", show_time=True):
                    for resultado in resultados_processados_para_salvar:
                        try:
                            salvar_saidas(
                                markdown=resultado['saida_markdown'],
                                latex=resultado['saida_latex'],
                                markdown_estruturado=resultado['markdown_estruturado'],
                                latex_estruturado=resultado['latex_estruturado'],
                                imagem_bytes=resultado['imagem_bytes']
                            )
                        except Exception as e:
                            st.error(f"Erro ao salvar um dos resultados no Firebase: {e}")
                st.success("Resultados salvos com sucesso no seu histórico!")
            elif not (hasattr(st, 'user') and st.user): # Verifica se o objeto st.user existe e se o usuário está logado
                st.warning("Faça login para que seus resultados sejam salvos no histórico.")
            # else: Se não há resultados processados, não faz nada.


# As variáveis `saida_final_latex` e `saida_final_markdown` devem usar as acumuladas para download
saida_final_latex = saidas_latex_acumuladas
saida_final_markdown = saidas_markdown_acumuladas


st.divider()
with st.spinner("Preparando downloads e exibição final...", show_time=True, width = "stretch"): # <--- MUDANÇA: Mensagem de spinner
    try:
        col3, col4 = st.columns(2)

        with col3:
            # <--- MUDANÇA: Usa a variável acumulada para display e download
            if saidas_latex_acumuladas:
                st.subheader('Código LaTeX Gerado (acumulado):') # <--- MUDANÇA: Título para clareza
                st.code(saidas_latex_acumuladas, language='latex', line_numbers=True, height=300)
                st.download_button(
                        label="Baixar código LaTeX",
                        data=saida_final_latex,
                        file_name="relatorio.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key ='download_latex'
                    )

        with col4:
            # <--- MUDANÇA: Usa a variável acumulada para display e download
            if saidas_markdown_acumuladas:
                st.subheader('Código Markdown Gerado (acumulado):') # <--- MUDANÇA: Título para clareza
                st.code(saidas_markdown_acumuladas, language='markdown', line_numbers=True, height=300)
                st.download_button(
                    label="Baixar código Markdown",
                    data=saida_final_markdown,
                    file_name="texto.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key ='download_markdown'
                    )
    except Exception as e:
        st.error(f"Erro ao gerar os códigos para download/exibição: {e}") # <--- MUDANÇA: Mensagem de erro mais específica