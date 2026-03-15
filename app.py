import streamlit as st
import pandas as pd
from agent.agent import ask_agent

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# ======================
# CSS MODERNO
# ======================

st.markdown("""
<style>

.main-title{
    font-size:32px;
    font-weight:700;
}

.subtitle{
    color:gray;
    margin-bottom:20px;
}

/* Card estilo SaaS */

.card{
    background-color:rgba(255,255,255,0.04);
    padding:20px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.08);
}

/* Insight */

.insight{
    font-size:16px;
    line-height:1.6;
}

/* Sidebar */

.sidebar-title{
    font-size:20px;
    font-weight:600;
}

/* Botões */

.stButton button{
    border-radius:8px;
    height:40px;
}

/* chat spacing */

[data-testid="stChatMessage"]{
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# SIDEBAR
# ======================

with st.sidebar:

    st.markdown("## 📊 AI Data Analyst")

    st.markdown("""
    **AI Assistant para análise de dados**

    Faça perguntas sobre seus dados
    e receba insights automaticamente.
    """)

    if st.button("🧹 Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("### Sobre")

    st.markdown("""
    Projeto de **AI Data Analyst**.

    Funcionalidades:

    • geração automática de SQL  
    • análise de dados com LLM  
    • gráficos automáticos  
    """)

# ======================
# MEMÓRIA DO CHAT
# ======================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# HEADER
# ======================

st.markdown('<div class="main-title">📊 AI Data Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pergunte qualquer coisa sobre os dados</div>', unsafe_allow_html=True)

# ======================
# HISTÓRICO
# ======================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "chart" in message and message["chart"] is not None:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.bar_chart(message["chart"])

            st.markdown('</div>', unsafe_allow_html=True)

# ======================
# INPUT DO USUÁRIO
# ======================

prompt = st.chat_input("Pergunte algo sobre os dados...")

if prompt:

    # mostrar pergunta
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # resposta do agente
    with st.chat_message("assistant"):

        with st.spinner("Analisando dados..."):

            insight, df = ask_agent(prompt)

        st.markdown(
            f'<div class="card insight">{insight}</div>',
            unsafe_allow_html=True
        )

        chart_data = None

        # gerar gráfico automático
        if isinstance(df, pd.DataFrame) and len(df.columns) >= 2:

            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:

                x_col = df.columns[0]
                y_col = numeric_cols[0]

                chart_data = df.set_index(x_col)[y_col]

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.bar_chart(chart_data)

                st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": insight,
        "chart": chart_data
    })