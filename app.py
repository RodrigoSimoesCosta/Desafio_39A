import streamlit as st
from chatbot_logic import Chatbot

# Configuração da página
st.set_page_config(page_title="Chatbot Marketplace", layout="centered")
st.title("🤖 Atendimento - Marketplace de Eletrônicos")

# Inicialização da sessão
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = Chatbot()
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []
if 'entrada_usuario' not in st.session_state:
    st.session_state.entrada_usuario = ""
if 'chatbot_encerrado' not in st.session_state:
    st.session_state.chatbot_encerrado = False

# Função que processa a entrada do usuário
def processar_entrada():
    entrada = st.session_state.entrada_usuario.strip()
    if entrada:
        resposta = st.session_state.chatbot.responder(entrada)
        st.session_state.mensagens.append(("Você", entrada))
        st.session_state.mensagens.append(("Bot", resposta))
        st.session_state.entrada_usuario = ""

# Estilo para o histórico com rolagem
chat_css = """
<style>
.chat-box {
    max-height: 400px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
}
.message {
    margin-bottom: 10px;
}
.user {
    text-align: right;
    font-weight: bold;
    color: #2c7be5;
}
.bot {
    text-align: left;
    font-weight: bold;
    color: #1c1c1c;
}
</style>
<script>
const chatBox = document.querySelector('.chat-box');
if (chatBox) {
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 100);
}
</script>
"""

st.markdown(chat_css, unsafe_allow_html=True)

# Botões de controle
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🔄 Reiniciar Chat"):
        st.session_state.chatbot = Chatbot()
        st.session_state.mensagens = []
        st.session_state.entrada_usuario = ""
        st.session_state.chatbot_encerrado = False

with col2:
    if st.button("❌ Fechar Bot"):
        st.session_state.chatbot_encerrado = True

# Verifica se o bot foi encerrado
if st.session_state.chatbot_encerrado:
    st.warning("🚫 O atendimento foi encerrado. Obrigado por nos visitar!")
else:
    # Container com rolagem
    mensagens_html = "<div><i>Estamos felizes em ter você aqui! Tudo bem com você?</i></div><br>"
    for autor, texto in st.session_state.mensagens:
        classe = "user" if autor == "Você" else "bot"
        mensagens_html += f"<div class='message {classe}'><b>{autor}:</b> {texto}</div>"

    st.markdown(f"<div class='chat-box'>{mensagens_html}</div>", unsafe_allow_html=True)

    # Campo de entrada no final
    st.text_input("Você:", key="entrada_usuario", on_change=processar_entrada)

# Botão extra para limpar chat sem reiniciar chatbot
#st.markdown("---")
#if st.button("🗑️ Limpar Chat"):
#    st.session_state.mensagens = []
