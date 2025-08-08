import streamlit as st
from datetime import date

st.title("Gamificação Minimalista")
st.caption("Exemplo simples de pontos, níveis, badges e check-in diário.")

# Estado inicial
if "gamificacao" not in st.session_state:
    st.session_state.gamificacao = {
        "points": 0,
        "level": 1,
        "badges": [],
        "streak_count": 0,
        "last_checkin": None,
    }

state = st.session_state.gamificacao

# Funções utilitárias
def compute_level(total_points: int) -> int:
    # Cada 100 pontos = +1 nível (1, 2, 3...)
    return max(1, 1 + total_points // 100)

def next_level_threshold(level: int) -> int:
    # Pontos totais necessários para o próximo nível
    return level * 100

def grant_badge(badge: str) -> None:
    if badge not in state["badges"]:
        state["badges"].append(badge)
        st.success(f"🏅 Novo badge: {badge}")

# Cabeçalho com informações
user_name = getattr(st.user, "name", "Você") if hasattr(st, "user") else "Você"
st.write(f"Bem-vindo(a), {user_name}!")

# Ações
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Concluir tarefa (+10 pts)"):
        state["points"] += 10

with col2:
    if st.button("📆 Check-in diário (+5 pts)"):
        today = date.today().isoformat()
        if state["last_checkin"] != today:
            state["last_checkin"] = today
            state["streak_count"] += 1
            state["points"] += 5
        else:
            st.info("Você já fez o check-in hoje.")

# Atualiza nível e progressão
new_level = compute_level(state["points"])
if new_level > state["level"]:
    state["level"] = new_level
    st.balloons()
    st.success(f"Parabéns! Você alcançou o nível {state['level']}.")

# Regras simples de badges
if state["points"] >= 10:
    grant_badge("Primeiros Passos (10 pts)")
if state["points"] >= 50:
    grant_badge("Aprendiz (50 pts)")
if state["points"] >= 100:
    grant_badge("Pro (100 pts)")
if state["streak_count"] >= 3:
    grant_badge("Foco 3 dias")
if state["streak_count"] >= 7:
    grant_badge("Consistência 7 dias")

# Exibição de status
st.subheader("Seu progresso")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Nível", state["level"])
with col_b:
    st.metric("Pontos", state["points"])
with col_c:
    st.metric("Streak (dias)", state["streak_count"])

needed_for_next = next_level_threshold(state["level"]) - state["points"]
base_of_level = next_level_threshold(state["level"] - 1) if state["level"] > 1 else 0
progress_in_level = state["points"] - base_of_level
level_span = next_level_threshold(state["level"]) - base_of_level
progress_ratio = 0.0 if level_span <= 0 else min(1.0, max(0.0, progress_in_level / level_span))

st.progress(progress_ratio, text=f"{progress_in_level}/{level_span} para o próximo nível")

# Badges
st.subheader("Badges conquistados")
if state["badges"]:
    for badge in state["badges"]:
        st.write(f"- 🏅 {badge}")
else:
    st.info("Nenhum badge ainda. Complete ações para ganhar seus primeiros!")

st.divider()
st.caption("Dica: este exemplo usa apenas `st.session_state`, então os dados não persistem entre sessões. Para produção, salve no seu banco (ex.: Firebase).")