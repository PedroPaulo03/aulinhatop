import streamlit as st
import numpy as np
from funcoes import(
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,   
)

  
st.title("✍️ Transforme Notas Manuscritas em LaTeX")

INSTRUCOES = """
você é um assistente de IA que converte anotações manuscritas em **LaTeX puro**  
seu objetivo é reproduzir o texto com **fidelidade total**, prestando atenção especial a:

1. **Equações inline**: identifique expressões matemáticas e envolva-as em `$...$`  
- ex: `E = m c^2` → `$E = m c^2$`

2. **Equações de exibição** (bloco): envolva em `$$...$$`  
- garanta uma linha em branco antes e depois  
- preserve quebras de linha internas  
- ex:  
    ```
    integral de a a b
    f(x) dx
    ```  
    →  
    $$
    \int_a^b f(x)\,dx
    $$

3. **Comandos LaTeX**: use sempre `\int`, `\sum`, subscritos `_{}`, sobrescritos `^{}` etc., sem simplificar ou omitir nada

4. **Texto normal**: mantenha parágrafos, espaçamentos e quebras de linha exatamente como no manuscrito

5. **Nada extra**: não adicione títulos, legendas, comentários ou qualquer texto além da conversão solicitada  
"""


INSTRUCOES_MARKDOWN = """
você é um assistente de IA que converte anotações manuscritas em markdown com suporte a LaTeX  
seu objetivo é reproduzir o texto exatamente, incluindo espaços e quebras de linha nas equações  

regras essenciais:
1. identifique expressões matemáticas inline e envolva-as em `$...$`, sem alterar espaçamentos internos  
2. equações em bloco devem ficar entre `$$...$$`  
- garanta uma linha em branco **antes e depois** de cada bloco de equação  
- preserve quebras de linha internas à equação como no original  
3. use comandos LaTeX (ex: `\\int`, subscrito `_{}`, sobrescrito `^{}`)  
4. preserve quebras de parágrafo e espaçamento entre blocos de texto  
5. não adicione observações, títulos ou comentários extras — apenas o texto formatado  

exemplos:
- `E = m c^2` → `$E = m c^2$`  
-                                                                                           
`integral de a a b  
f(x) dx`  

→  

$$
\int_a^b f(x)\,dx
$$  
"""

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
        if st.button("Processar Imagem e Gerar Códigos", key="process_button"):
            # Garante que o arquivo foi carregado antes de processa
            saidas_latex = ''  # Variável para armazenar as saídas LaTeX
            saidas_markdown = ''  # Variável para armazenar as saídas Markdown
            for i, imagem_carregada in enumerate(imagens_carregadas):
                
                if imagem_carregada.getvalue():
                    
                    with st.spinner(f"Convertendo texto da página {i+1} para Markdown e LaTeX...", show_time=True):
                        file_bytes = imagem_carregada.getvalue()
                        try: 
                            saida_latex = generate(file_bytes, type=imagem_carregada.type)
                            saidas_latex += saida_latex + "\n\n"

                            saida_markdown = gerar_markdown(file_bytes, type=imagem_carregada.type)
                            saidas_markdown += saida_markdown + '''  
'''
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
            saida_final_latex = estruturar_latex(saidas_latex)
            saida_final_markdown = estruturar_markdown(saidas_markdown)

st.divider()

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
            key ='download_markdown'  # Adiciona uma chave única para evitar conflitos           
            )



