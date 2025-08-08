import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.title("Exemplos CRUD - Firebase")

# Conectar Firebase
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

# CREATE - Criar documento
st.header("Guarde os dados do usuário")
#nome = st.text_input("Nome")
if st.button("Salvar info do usuario"):
    # Usa email do usuário como ID
    informacoes = {'nome': st.user.name,
                    'foto': st.user.picture,
                    'email': st.user.email,
                    'hora': datetime.now().strftime("%H:%M:%S")}
    db.collection(colecao).add(informacoes)
    st.write("Informações salvas com sucesso")


# READ - Ler documentos  
st.header("READ")
if st.button("Listar todos"):
    docs = db.collection(colecao).stream()
    for doc in docs:
        st.write(f"{doc.id}: {doc.to_dict()}")

# UPDATE - Atualizar documento
st.header("UPDATE")
doc_id = st.text_input("ID do documento")
novo_nome = st.text_input("Novo nome")
if st.button("Atualizar"):
    db.collection(colecao).document(doc_id).update({'nome': novo_nome})
    st.write("Atualizado!")

# DELETE - Deletar documento
st.header("DELETE")  
id_deletar = st.text_input("ID para deletar")
if st.button("Deletar"):
    db.collection(colecao).document(id_deletar).delete()
    st.write("Deletado!")

st.header("📚 Outros métodos úteis do Firebase")

# CONTADOR - Sistema simples de contagem
st.subheader("🔢 Contador Pessoal")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Incrementar"):
        user_ref = db.collection(colecao).document(st.user.email)
        doc = user_ref.get()
        dados = doc.to_dict() if doc.exists else {}
        contador_atual = dados.get('contador', 0)
        dados['contador'] = contador_atual + 1
        user_ref.set(dados)
        st.rerun()

with col2:
    if st.button("🔍 Ver contador"):
        doc = db.collection(colecao).document(st.user.email).get()
        dados = doc.to_dict() if doc.exists else {}
        total = dados.get('contador', 0)
        st.metric("Seu contador", total)

# NOTAS - Sistema de anotações
st.subheader("📝 Notas Rápidas")
nova_nota = st.text_input("Nova nota")
if st.button("💾 Salvar nota"):
    from datetime import datetime
    user_ref = db.collection(colecao).document(st.user.email)
    doc = user_ref.get()
    dados = doc.to_dict() if doc.exists else {}
    
    if 'notas' not in dados:
        dados['notas'] = []
    
    dados['notas'].append({
        'texto': nova_nota,
        'horario': datetime.now().strftime('%d/%m %H:%M')
    })
    user_ref.set(dados)
    st.success("Nota salva!")

if st.button("📋 Ver minhas notas"):
    doc = db.collection(colecao).document(st.user.email).get()
    dados = doc.to_dict() if doc.exists else {}
    notas = dados.get('notas', [])
    
    if notas:
        for nota in notas:  
            st.write(f"📝 {nota['horario']}: {nota['texto']}")
    else:
        st.info("Nenhuma nota ainda")

# ESTATÍSTICAS - Análise simples
st.subheader("📊 Estatísticas")
if st.button("Total de usuários"):
    docs = list(db.collection(colecao).stream())
    st.metric("Total de usuários", len(docs))


st.divider()

# funções para carregar uma nota específica no sistema como se fosse uma avaliacao. 
# é necessario guardar o campo para cada usuario na base de dados e salvar a informacao
# sempre que o usuario clicar no botao st.feedback, deve guardar a nota que ele deu
# se ele muda a avaliação, deve atualizar o campo na base de dados
# se o usuario nao avaliou, deve mostrar a mensagem "Avalie este conteúdo"

st.header("⭐ Avalie este conteúdo")
nota_atual = 0      
doc = db.collection(colecao).document(st.user.email).get()
if doc.exists:
    dados = doc.to_dict()
    nota_atual = dados.get('nota_avaliacao', 0) 
    if nota_atual > 0:
        st.write(f"Você avaliou este conteúdo com {nota_atual} estrelas.")
    else:
        st.write("Avalie este conteúdo")    
        nota = st.slider("Sua avaliação", 0, 5, nota_atual, step=1)
        if st.button("Enviar avaliação"):
            db.collection(colecao).document(st.user.email).update({'nota_avaliacao': nota})
            st.success("Avaliação salva!")
            st.rerun()
