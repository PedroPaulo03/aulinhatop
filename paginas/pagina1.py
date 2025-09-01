import streamlit as st
from typing import List

# Supondo que o módulo 'funcoes' exista e contenha a função 'gerar_estruturado'
# from funcoes import gerar_estruturado

# ----- MOCKUP DA FUNÇÃO DE PROCESSAMENTO (PARA TESTES) -----
# Se você remover o comentário da linha acima, pode remover esta função.
def gerar_estruturado(file_bytes, type):
    """Função de exemplo para simular o processamento."""
    content = f"Conteúdo processado para o arquivo de tipo {type}."
    saida_markdown = f"## Título (Markdown)\n{content}"
    saida_latex = f"\\documentclass{{article}}\n\\begin{document}}\n\\section*{{Título (LaTeX)}}\n{content}\n\\end{{document}}"
    return saida_markdown, saida_latex
# -----------------------------------------------------------

# Definição da classe para uma saída estruturada
class ResultadoProcessamento:
    def __init__(self, nome_arquivo: str, saida_markdown: str, saida_latex: str):
        self.nome_arquivo = nome_arquivo
        self.markdown = saida_markdown
        self.latex = saida_latex

# Configuração da página
st.set_page_config(layout="wide")
  
st.title("✍️ Transforme seus textos escritos em formato LaTeX")
st.info("Instruções: Este aplicativo foi projetado para digitalizar textos e fórmulas matemáticas manuscritas, convertendo-os diretamente para o formato LaTeX e Markdown.")

# Inicializar o estado da sessão para armazenar os resultados
if 'resultados' not in st.session_state:
    st.session_state.resultados: List[ResultadoProcessamento] = []

# --- Coluna 1: Upload e Pré-visualização ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Carregue suas imagens")
        imagens_carregadas = st.file_uploader(
            "Selecione uma ou mais imagens (.png, .jpeg, .jpg)",
            type=["png", "jpeg", "jpg"],
            accept_multiple_files=True
        )

        if not imagens_carregadas:
            st.info("Por favor, carregue uma ou mais imagens para começar.")
        else:
            st.subheader('Pré-visualização')
            # Selectbox para escolher qual imagem visualizar
            imagem_visualizada = st.selectbox(
                label='Selecione uma imagem para pré-visualizar:',
                options=imagens_carregadas,
                format_func=lambda img: img.name, # Mostra o nome do arquivo na caixa de seleção
                label_visibility='collapsed'
            )
            if imagem_visualizada:
                st.image(imagem_visualizada.getvalue(), caption=f"Visualizando: {imagem_visualizada.name}", use_container_width=True)

    # --- Coluna 2: Botão de Processamento e Visualização do Markdown ---
    with col2:
        st.subheader("2. Processe as imagens")
        if st.button("Gerar Códigos LaTeX e Markdown", use_container_width=True, type="primary", disabled=not imagens_carregadas):
            st.session_state.resultados = []  # Limpa resultados anteriores
            
            with st.spinner("Processando imagens... Isso pode levar alguns segundos."):
                for imagem in imagens_carregadas:
                    try:
                        file_bytes = imagem.getvalue()
                        # Chama a função de processamento que retorna os dois formatos
                        saida_md, saida_tex = gerar_estruturado(file_bytes, type=imagem.type)
                        
                        # Cria um objeto estruturado e adiciona à lista no session_state
                        resultado = ResultadoProcessamento(
                            nome_arquivo=imagem.name,
                            saida_markdown=saida_md,
                            saida_latex=saida_tex
                        )
                        st.session_state.resultados.append(resultado)
                        
                    except Exception as e:
                        st.error(f"Erro ao processar o arquivo '{imagem.name}': {e}")
            st.success("Processamento concluído com sucesso!")

        # Exibe a pré-visualização do Markdown se houver resultados
        if st.session_state.resultados:
            st.markdown("---")
            st.subheader("3. Pré-visualização do Conteúdo")
            # Concatena todos os markdowns para uma visualização única
            preview_markdown = "\n\n---\n\n".join([res.markdown for res in st.session_state.resultados])
            with st.container(height=400): # Container com altura fixa e barra de rolagem
                st.markdown(preview_markdown)

st.divider()

# --- Seção de Resultados: Códigos e Botões de Download ---
if st.session_state.resultados:
    st.subheader("4. Códigos Gerados")
    
    # Agrupa todo o conteúdo para download
    saida_final_latex = "\n\n".join([res.latex for res in st.session_state.resultados])
    saida_final_markdown = "\n\n".join([res.markdown for res in st.session_state.resultados])

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader('Código LaTeX Completo')
        st.code(saida_final_latex, language='latex', line_numbers=True)
        st.download_button(
            label="Baixar código LaTeX (.tex)",
            data=saida_final_latex.encode('utf-8'),
            file_name="codigo_latex.tex",
            mime="text/plain",
            use_container_width=True
        )

    with col4:
        st.subheader('Código Markdown Completo')
        st.code(saida_final_markdown, language='markdown', line_numbers=True)
        st.download_button(
            label="Baixar código Markdown (.md)",
            data=saida_final_markdown.encode('utf-8'),
            file_name="codigo_markdown.md",
            mime="text/markdown",
            use_container_width=True
        )