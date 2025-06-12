import streamlit as st
from chatbot_rag import Chatbot

# Inicializar o chatbot na sessão (evita reinicialização a cada nova mensagem)
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = Chatbot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chatbot RAG - Loja Tech", page_icon="🤖")

st.title("🛍️ Chatbot Loja Tech com RAG")
st.markdown("Converse com o assistente para encontrar o produto ideal!")

# Campo de entrada do usuário
mensagem_usuario = st.text_input("Digite sua mensagem:", "")

# Enviar mensagem
if st.button("Enviar") or (mensagem_usuario and not st.session_state.chat_history):
    if mensagem_usuario.strip():
        resposta = st.session_state.chatbot.responder(mensagem_usuario)
        st.session_state.chat_history.append(("Você", mensagem_usuario))
        st.session_state.chat_history.append(("Bot", resposta))
        st.experimental_rerun()

# Exibir histórico de conversa
if st.session_state.chat_history:
    for autor, msg in st.session_state.chat_history:
        st.markdown(f"**{autor}:** {msg}")
