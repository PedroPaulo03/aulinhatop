import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from PIL import Image
import io
import base64

# Conectar ao Firebase
@st.cache_resource
def conectar_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

    db = conectar_firebase()
    colecao = 'usuarios2'

st.title("📚 Minhas Conversas Matemáticas")

if st.user:
    user_ref = db.collection(colecao).document(st.user.email)
    doc = user_ref.get()
    dados = doc.to_dict() if doc.exists else {}

    if 'conversas' not in dados:
        dados['conversas'] = []

    # Upload de imagem
    imagem = st.file_uploader("Envie uma imagem com a questão", type=["png", "jpg", "jpeg"])
    
    if imagem and st.button("🔍 Processar imagem"):
        # Simula resposta em LaTeX (substitua pelo seu modelo real)
        resposta_latex = r"f(x) = \int_{0}^{x} e^{-t^2} dt"

        # Codifica imagem para base64 para salvar como texto no Firebase
        bytes_imagem = imagem.read()
        imagem_base64 = base64.b64encode(bytes_imagem).decode("utf-8")

        # Adiciona ao histórico
        dados['conversas'].add({
            'imagem': imagem_base64,
            'resposta_latex': resposta_latex,
            'horario': datetime.now().strftime("%d/%m %H:%M")
        })

        user_ref.set(dados)
        st.success("Resposta gerada e salva no histórico.")
        st.rerun()

    st.divider()
    st.subheader("📜 Histórico de Imagens e Respostas")

    conversas = dados.get('conversas', [])

    if not conversas:
        st.info("Nenhuma conversa salva ainda.")
    else:
        for item in reversed(conversas):
            st.markdown(f"🕒 {item['horario']}")
            # Decodifica imagem base64 e mostra
            img_bytes = base64.b64decode(item['imagem'])
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, caption="Imagem enviada", use_container_width=True)

            # Renderiza resposta em LaTeX
            st.latex(item['resposta_latex'])

else:
    st.warning("Você precisa estar logado para usar esta funcionalidade.")



if st.sidebar.button("Log out"):
    st.logout()
