import streamlit as st
from google import genai
from google.genai import types
from funcoes import(
    generate,
    gerar_markdown,
    estruturar_latex,
    estruturar_markdown,   
)

# Configuração do cliente Gemini
client = genai.Client()

st.set_page_config(layout="wide")
st.title("✍️ Transforme seus textos escritos em formato LaTeX")
st.info("Carregue uma imagem única (para pré-visualização) e/ou várias imagens (para ordenação e transformação em LaTeX).")

# Layout 2 colunas
col1, col2 = st.columns(2)

# --------------------------
# COLUNA 1 = Imagem única
# --------------------------
with col1:
    st.subheader("📌 Pré-visualização de uma imagem")
    imagem_unica = st.file_uploader(
        "Selecione apenas uma imagem (.png, .jpeg, .jpg)",
        type=["png", "jpeg", "jpg"],
        accept_multiple_files=False,
        key="imagem_unica"
    )
    if imagem_unica:
        st.image(imagem_unica.getvalue(), caption="Imagem selecionada", use_container_width=True)

# --------------------------
# COLUNA 2 = Várias imagens
# --------------------------
with col2:
    st.subheader("📚 Upload de várias imagens (ordem inferida pelo Gemini)")
    imagens_multiplas = st.file_uploader(
        "Carregue várias imagens (.png, .jpeg, .jpg)",
        type=["png", "jpeg", "jpg"],
        accept_multiple_files=True,
        key="imagens_multiplas"
    )

    if imagens_multiplas and len(imagens_multiplas) > 1:
        if st.button("Processar e Ordenar Imagens", use_container_width=True):
            partes = []

            for imagem in imagens_multiplas:
                img_bytes = imagem.getvalue()
                partes.append(
                    types.Part.from_bytes(
                        data=img_bytes,
                        mime_type="image/jpeg" if imagem.type == "image/jpeg" else "image/png"
                    )
                )

            with st.spinner("Inferindo ordem e transformando em LaTeX..."):
                try:
                    resposta = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            "Estas imagens foram tiradas em ordem aleatória de um quadro. Por favor, organize-as na ordem correta e depois extraia todo o conteúdo em formato LaTeX e Markdown.",
                            *partes
                        ]
                    )

                    saida_texto = resposta.text

                    # Aqui você pode separar LaTeX e Markdown se quiser
                    saida_final_latex = estruturar_latex(saida_texto)
                    saida_final_markdown = estruturar_markdown(saida_texto)

                    st.markdown("### ✅ Resultado Ordenado")
                    st.markdown(saida_final_markdown)

                    # Botões de download
                    st.download_button(
                        "Baixar LaTeX",
                        data=saida_final_latex,
                        file_name="saida_latex.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    st.download_button(
                        "Baixar Markdown",
                        data=saida_final_markdown,
                        file_name="saida_markdown.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Erro ao processar imagens: {e}")


