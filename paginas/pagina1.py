import streamlit as st
import numpy as np
from funcoes import(
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,   
)

st.set_page_config(layout = "wide")
  
st.title("✍️ Transforme seus textos escritos em formato LaTeX")
st.info("Instruções: Este app foi pensando para atenter as seguintes pessoas: o monitor, professor, aluno e pesquisador que ao fazer algo de maneira escrita na mão grande no papel, quadro ou tablet, que contenha fórmulas matemáticas dutante o texto e tem interesse em digitalizar o arquivo, passando assim para o formato LateX, e é nessa prte que entramos, preparamos a escrita no LateX para você.")


imagens_carregadas = st.file_uploader(
    "Selecione uma imagem (.png, .jpeg, .jpg) )",
    type=["png", "jpeg", "jpg"],
    accept_multiple_files=True # Para este exemplo, apenas um arquivo por vez
)

if imagens_carregadas is None or len(imagens_carregadas) == 0:
    st.info("Por favor, carregue uma imagem para começar.")

col1, col2 = st.columns(2)

with col1:
    if imagens_carregadas is True or len(imagens_carregadas) != 0:
        st.subheader('Pré-visualização da imagem')
        imagem_visualizada = st.selectbox(label='Selecione a imagem para pré-visualização',
                                        format_func=lambda img: img.name if img else "Arquivo desconhecido",
                                        options = imagens_carregadas, index = 0, label_visibility='hidden')
    else:
        imagem_visualizada = None
    if imagem_visualizada is not None:
        imagem_bytes = imagem_visualizada.getvalue()
        st.image(imagem_bytes, caption="Imagem selecionada", use_container_width=True)


# if imagens_carregadas is not None:
#     with col1:
#         st.subheader("Pré-visualização da Imagem:")
#         # Exibe a imagem carregada. Para PDF, mostrará apenas a primeira página.
#         st.image(imagens_carregadas, caption="Sua imagem carregada")#, width =300)

# Definindo as variáveis para evitar erros em col3 e col4

saidas_latex = None
saidas_markdown = None

with col2:
    if imagens_carregadas and len(imagens_carregadas) > 0:  
        if st.button("Processar Imagem e Gerar Códigos", key="process_button", use_container_width=True):
            # Garante que o arquivo foi carregado antes de processa
            saidas_latex = ''  # Variável para armazenar as saídas LaTeX
            saidas_markdown = ''  # Variável para armazenar as saídas Markdown
            for i, imagem_carregada in enumerate(imagens_carregadas):
                
                if imagem_carregada.getvalue():
                    
                    with st.spinner(f"Convertendo texto da página {i+1} para Markdown e LaTeX...", show_time=True):
                        file_bytes = imagem_carregada.getvalue()
                        try: 
                            saida_markdown, saida_latex = gerar_estruturado(file_bytes, type=imagem_carregada.type)
                            saidas_markdown += saida_markdown + "\n\n"
                            saidas_latex += saida_latex + "\n\n"

                        except Exception as e:
                            st.error(f"Erro ao processar a imagem: {e}")
                                
                else:
                        st.warning("Nenhum arquivo válido foi carregado para processamento.")

            # Exibir o resultado em LaTeX
            st.markdown("---")
            st.subheader("Visualização:")             
            # st.markdown(saidas)
            st.markdown(saidas_markdown)
            # Baixar o resultado em LaTeX e Markdown
            saida_final_latex = saidas_latex
            saida_final_markdown = saidas_markdown

st.divider()
with st.spinner("Gerando códigos", show_time=True, width = "stretch"):
    try:
        col3, col4 = st.columns(2)

        with col3:
            if saidas_latex:
                st.subheader('Código LaTeX gerado:')
                st.code(saidas_latex, language='latex', line_numbers=True, height=300)
                st.download_button(
                        label="Baixar código LaTeX",
                        data=saida_final_latex,            # sua string de texto
                        file_name="relatorio.txt",   # extensão .txt
                        mime="text/plain",
                        use_container_width=True,
                        key ='download_latex'  # Adiciona uma chave única para evitar conflitos  
                    )

        with col4:
            if saidas_markdown:
                st.subheader('Código Markdown gerado:')
                st.code(saidas_markdown, language='markdown', line_numbers=True, height=300)
                st.download_button(
                    label="Baixar código Markdown",
                    data=saida_final_markdown,            # sua string de texto
                    file_name="texto.md",   # extensão .md
                    mime="text/markdown",
                    use_container_width=True,
                    key ='download_markdown'  # Adiciona uma chave única para evitar conflitos           
                    )
    except Exception as e:
        st.error(f"Erro ao gerar os códigos:{e}")


