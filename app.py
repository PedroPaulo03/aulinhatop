import streamlit as st

if not hasattr(st.user, 'is_logged_in') or not st.user.is_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo centralizada
        st.image('imagelatex/capa.jpg', use_container_width=True)
        st.title("Escrivão de LaTeX") 
        st.markdown("Faça login com sua conta Google")

        # Botão de login
        if st.button("Login com Google", type="primary", use_container_width=True, icon=':material/login:'):
            st.login()  # redireciona para o login do Streamlit
else:
    st.success(f"Oi, {getattr(st.user, 'name', 'Usuário')}! ✅")
    st.write("Você está logado. Use o menu lateral para acessar as ferramentas.")