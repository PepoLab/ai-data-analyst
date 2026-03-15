import streamlit as st
import pandas as pd
from agent.agent import ask_agent

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CSS PROFISSIONAL
# -------------------------

st.markdown("""
<style>

body {
    font-family: Inter, sans-serif;
}

.main-title{
    font-size:34px;
    font-weight:700;
}

.subtitle{
    color:#9ca3af;
    margin-bottom:20px;
}

/* CARD INSIGHT */

.insight-card{
    background-color:#111827;
    padding:20px;
    border-radius:10px;
    border:1px solid #374151;
    font-size:16px;
}

/* CHAT */

[data-testid="stChatMessage"]{
    margin-bottom:15px;
}

/* INPUT */

.stChatInput input{
    border-radius:12px;
}

/* SIDEBAR */

.sidebar-title{
    font-size:20px;
    font-weight:600;
}

/* BOTÃO */

.stButton button{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.markdown("## 📊 AI Data Analyst")

    st.markdown("""
AI assistant para análise de dados.

Pergunte sobre seu dataset e receba:

• insights automáticos  
• análises rápidas  
• gráficos instantâneos  
""")

    st.markdown("---")

    if st.button("🧹 Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("Dataset ativo:")

    st.success("vendas.db")

# -------------------------
# HEADER
# -------------------------

st.markdown('<div class="main-title">AI Data Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pergunte qualquer coisa sobre seus dados</div>', unsafe_allow_html=True)

# -------------------------
# HISTÓRICO CHAT
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg.get("chart") is not None:
            st.bar_chart(msg["chart"])

# -------------------------
# INPUT
# -------------------------

prompt = st.chat_input("Pergunte algo sobre os dados...")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("assistant"):

        with st.spinner("Analisando dados..."):

            insight, df = ask_agent(prompt)

        st.markdown(
            f'<div class="insight-card">{insight}</div>',
            unsafe_allow_html=True
        )

        chart_data = None

        if isinstance(df, pd.DataFrame) and len(df.columns) >= 2:

            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:

                x_col = df.columns[0]
                y_col = numeric_cols[0]

                chart_data = df.set_index(x_col)[y_col]

                st.bar_chart(chart_data)

    st.session_state.messages.append({
        "role": "assistant",
        "content": insight,
        "chart": chart_data
    })