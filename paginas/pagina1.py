import streamlit as st

# Protege o conteúdo se não estiver logado
if not hasattr(st.user, "is_logged_in") or not st.user.is_logged_in:
    st.warning("⚠️ Você precisa estar logado para acessar esta página.")
    st.stop()

# Conteúdo da página
st.title("✍️ Transforme Notas Manuscritas em LaTeX")
st.write("Aqui está sua ferramenta!")