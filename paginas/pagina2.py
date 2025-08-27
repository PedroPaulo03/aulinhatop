import streamlit as st
import numpy as np
from datetime import datetime
from PIL import Image
import io
import base64

from funcoes import (
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,
    conectar_firebase,
    salvar_saidas
)

# Config
st.set_page_config(layout="wide")
st.title("✍️ Transforme seus textos escritos em formato LaTeX")

db = conectar_firebase()
colecao = 'usuarios2'

if st.user:
    user_ref = db.collection(colecao).document(st.user.email)
    doc = user_ref.get()
    dados = doc.to_dict() if doc.exists else {}

    if 'conversas' not in dados:
        dados['conversas'] = []

    # Upload de imagens
    imagens_carregadas = st.file_uploader(
        "Selecione uma ou mais imagens (.png, .jpeg, .jpg)",
        type=["png", "jpeg", "jpg"],
        accept_multiple_files=True
    )

    if imagens_carregadas is None or len(imagens_carregadas) == 0:
        st.info("Por favor, carregue uma imagem para começar.")

    col1, col2 = st.columns(2)

    # Pré-visualização
    with col1:
        if imagens_carregadas and len(imagens_carregadas) > 0:
            st.subheader('Pré-visualização da imagem')
            imagem_visualizada = st.selectbox(
                label='Selecione a imagem para pré-visualização',
                format_func=lambda img: img.name if img else "Arquivo desconhecido",
                options=imagens_carregadas,
                index=0,
                label_visibility='hidden'
            )
        else:
            imagem_visualizada = None

        if imagem_visualizada is not None:
            imagem_bytes = imagem_visualizada.getvalue()
            st.image(imagem_bytes, caption="Imagem selecionada", use_container_width=True)

    # Processamento
    saidas_latex = None
    saidas_markdown = None

    with col2:
        if imagens_carregadas and len(imagens_carregadas) > 0:
            if st.button("Processar Imagem e Gerar Códigos", key="process_button", use_container_width=True):
                saidas_latex = ''
                saidas_markdown = ''
                for i, imagem_carregada in enumerate(imagens_carregadas):
                    if imagem_carregada.getvalue():
                        with st.spinner(f"Convertendo texto da página {i+1} para Markdown e LaTeX..."):
                            file_bytes = imagem_carregada.getvalue()
                            try:
                                saida_latex = generate(file_bytes, type=imagem_carregada.type)
                                saidas_latex += saida_latex + "\n\n"

                                saida_markdown = gerar_markdown(file_bytes, type=imagem_carregada.type)
                                saidas_markdown += saida_markdown + "\n"

                                # Salva cada imagem + latex no Firebase
                                imagem_base64 = base64.b64encode(file_bytes).decode("utf-8")
                                dados['conversas'].append({
                                    'imagem': imagem_base64,
                                    'resposta_latex': saida_latex,
                                    'horario': datetime.now().strftime("%d/%m %H:%M")
                                })
                                user_ref.set(dados)

                            except Exception as e:
                                st.error(f"Erro ao processar a imagem: {e}")

                # Exibir visualização
                st.markdown("---")
                st.subheader("Visualização (Markdown):")
                st.markdown(saidas_markdown)

                # Preparar para download
                saida_final_latex = estruturar_latex(saidas_latex)
                saida_final_markdown = estruturar_markdown(saidas_markdown)

                col3, col4 = st.columns(2)
                with col3:
                    if saidas_latex:
                        st.subheader('Código LaTeX gerado:')
                        st.code(saidas_latex, language='latex', line_numbers=True, height=300)
                        st.download_button(
                            label="Baixar código LaTeX",
                            data=saida_final_latex,
                            file_name="relatorio.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key='download_latex'
                        )
                with col4:
                    if saidas_markdown:
                        st.subheader('Código Markdown gerado:')
                        st.code(saidas_markdown, language='markdown', line_numbers=True, height=300)
                        st.download_button(
                            label="Baixar código Markdown",
                            data=saida_final_markdown,
                            file_name="texto.md",
                            mime="text/markdown",
                            use_container_width=True,
                            key='download_markdown'
                        )

    st.divider()
    st.subheader("📜 Histórico de Imagens e Respostas")
    conversas = dados.get('conversas', [])
    if not conversas:
        st.info("Nenhuma conversa salva ainda.")
    else:
        for item in reversed(conversas):
            st.markdown(f"🕒 {item['horario']}")
            img_bytes = base64.b64decode(item['imagem'])
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, caption="Imagem enviada", use_column_width=True)
            st.latex(item['resposta_latex'])

    salvar_saidas(markdown = saidas_markdown, latex = saidas_latex, markdown_estruturado = saida_final_markdown, latex_estruturado = saida_final_latex)


else:
    st.warning("Você precisa estar logado para usar esta funcionalidade.")

if st.sidebar.button("Log out"):
    st.logout()
