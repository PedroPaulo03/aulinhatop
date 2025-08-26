import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Conecta ao Firebase
@st.cache_resource
def conectar_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = conectar_firebase()
colecao = 'usuarios2'  # Nome da coleção no Firestore

# Título da página
st.title("👤 Meu Perfil e Histórico")

# Verifica se o usuário está logado
if st.user:
    st.subheader("Informações do Usuário")
    st.image(st.user.picture, width=100)
    st.write(f"**Nome:** {st.user.name}")
    st.write(f"**Email:** {st.user.email}")

    # Pega o documento do usuário no Firestore
    user_ref = db.collection(colecao).document(st.user.email)
    doc = user_ref.get()
    dados = doc.to_dict() if doc.exists else {}

    # Exibir o histórico de conversas
    st.subheader("💬 Histórico de Conversas")
    historico = dados.get('conversas', [])

    if historico:
        for item in historico:
            st.markdown(f"**{item['data']}** — {item['mensagem']}")
    else:
        st.info("Você ainda não possui conversas salvas.")
else:
    st.warning("Você precisa estar logado para ver esta página.")





if st.sidebar.button("Log out"):
    st.logout()
