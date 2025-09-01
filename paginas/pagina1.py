import streamlit as st
import numpy as np
import time
from typing import List, Optional
from pydantic import BaseModel
from funcoes import(
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,
    gerar_estruturado
)
from typing import List

st.set_page_config(layout="wide")

st.title("✍️ Conversor Inteligente para LaTeX & Markdown")
st.markdown("Use o **Modo Simples** para converter uma única imagem ou o **Modo Inteligente** para carregar várias imagens fora de ordem e deixar a IA organizá-las para você.")

# Inicializar o session_state para cada modo
if 'resultado_simples' not in st.session_state:
    st.session_state.resultado_simples: Optional[SaidaSimples] = None
if 'resultado_unificado' not in st.session_state:
    st.session_state.resultado_unificado: Optional[SaidaUnificada] = None


col1, col2 = st.columns(2)

# --- COLUNA 1: MODO SIMPLES (UMA IMAGEM) ---
with col1:
    st.header("1️⃣ Modo Simples")
    st.info("Carregue uma única imagem para conversão direta.")

    imagem_unica = st.file_uploader(
        "Selecione uma imagem (.png, .jpeg, .jpg)",
        type=["png", "jpeg", "jpg"],
        key="uploader_simples"
    )

    if imagem_unica:
        st.image(imagem_unica, caption="Imagem carregada.", use_container_width=True)

    if st.button("Transformar Imagem Única", use_container_width=True, disabled=not imagem_unica):
        with st.spinner("Processando a imagem..."):
            # Substitua pela sua chamada real
            st.session_state.resultado_simples = mock_gerar_saida_simples(imagem_unica.getvalue(), imagem_unica.name)
    
    # Exibição dos resultados do modo simples
    if st.session_state.resultado_simples:
        st.divider()
        st.subheader("Resultado (Modo Simples)")
        
        res_simples = st.session_state.resultado_simples
        
        st.markdown("### Pré-visualização (Markdown)")
        st.markdown(res_simples.markdown, unsafe_allow_html=True)

        st.code(res_simples.latex, language='latex', line_numbers=True)
        st.download_button("Baixar LaTeX", res_simples.latex, file_name="unico.tex", use_container_width=True)


# --- COLUNA 2: MODO INTELIGENTE (MÚLTIPLAS IMAGENS) ---
with col2:
    st.header("🧠 Modo Inteligente")
    st.info("Carregue várias imagens de um quadro ou caderno. A IA irá inferir a ordem correta e unificar o conteúdo.")
    
    imagens_multiplas = st.file_uploader(
        "Selecione as imagens (limite de 10)",
        type=["png", "jpeg", "jpg"],
        accept_multiple_files=True,
        key="uploader_multiplo"
    )

    if len(imagens_multiplas) > 10:
        st.warning("Limite de 10 imagens excedido. Apenas as 10 primeiras serão processadas.")
        imagens_multiplas = imagens_multiplas[:10]

    if imagens_multiplas:
        st.success(f"{len(imagens_multiplas)} imagens carregadas. Pronto para processar!")

    if st.button("Ordenar e Unificar Imagens", use_container_width=True, type="primary", disabled=len(imagens_multiplas) < 2):
        with st.spinner("Analisando, ordenando e unificando as imagens... Isso pode levar um momento."):
            # Substitua pela sua chamada real
            st.session_state.resultado_unificado = mock_ordenar_e_unificar_imagens(imagens_multiplas)

    # Exibição dos resultados do modo inteligente
    if st.session_state.resultado_unificado:
        st.divider()
        st.subheader("Resultado Unificado (Modo Inteligente)")
        
        res_unificado = st.session_state.resultado_unificado
        
        st.markdown("#### Ordem Inferida pela IA:")
        ordem_formatada = " ➔ ".join(f"`{nome}`" for nome in res_unificado.ordem_inferida)
        st.markdown(ordem_formatada)
        
        st.markdown("#### Pré-visualização do Documento Completo")
        with st.container(height=300):
            st.markdown(res_unificado.markdown_completo)
            
        st.markdown("#### Códigos Completos")
        tab_latex, tab_md = st.tabs(["LaTeX Completo", "Markdown Completo"])
        
        with tab_latex:
            st.code(res_unificado.latex_completo, language='latex', line_numbers=True)
            st.download_button("Baixar LaTeX Unificado", res_unificado.latex_completo, file_name="documento_unificado.tex", use_container_width=True)
        
        with tab_md:
            st.code(res_unificado.markdown_completo, language='markdown', line_numbers=True)
            st.download_button("Baixar Markdown Unificado", res_unificado.markdown_completo, file_name="documento_unificado.md", use_container_width=True)