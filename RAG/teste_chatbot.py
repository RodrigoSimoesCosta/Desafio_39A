# test_chatbot.py
from chatbot_rag import Chatbot

chatbot = Chatbot()

# Simulação de interações com o chatbot
print(chatbot.responder("Olá"))
print(chatbot.responder("Meu nome é João"))
print(chatbot.responder("Meu e-mail é joao@example.com"))
print(chatbot.responder("Meu telefone é 987654321"))
print(chatbot.responder("Estou procurando um smartphone"))
print(chatbot.responder("Quero um com boa câmera"))
print(chatbot.responder("Quanto custa?"))
