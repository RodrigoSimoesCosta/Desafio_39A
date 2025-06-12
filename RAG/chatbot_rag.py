# chatbot_rag.py
import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
from product_data import product_data

# Carregar a chave da API do OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Carregar o índice FAISS
index = faiss.read_index("product_index.faiss")

# Carregar os dados dos produtos
with open("product_data.npy", "rb") as f:
    product_data = np.load(f, allow_pickle=True)

# Função para gerar embeddings
def get_embedding(text):
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Função para recuperar produtos relevantes
def retrieve_products(query, k=3):
    query_embedding = np.array([get_embedding(query)]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    return [product_data[i] for i in indices[0]]

class Chatbot:
    def __init__(self):
        self.estado = "inicial"
        self.nome = None
        self.email = None
        self.telefone = None
        self.categoria_interesse = None
        self.produto_sugerido = None
        self.aguardando_preferencia = False

    def responder(self, mensagem):
        msg = mensagem.lower().strip()

        if self.estado == "inicial":
            self.estado = "aguardando_nome"
            return "Qual é o seu nome?"

        elif self.estado == "aguardando_nome":
            self.nome = mensagem.strip()
            self.estado = "aguardando_email"
            return f"Perfeito, {self.nome}! Qual é o seu e-mail?"

        elif self.estado == "aguardando_email":
            if "@" not in mensagem or "." not in mensagem:
                return "Esse e-mail parece inválido. Pode verificar e enviar novamente?"
            self.email = mensagem.strip()
            self.estado = "aguardando_telefone"
            return "E o seu telefone?"

        elif self.estado == "aguardando_telefone":
            telefone_limpo = re.sub(r'\D', '', mensagem)
            if len(telefone_limpo) < 8:
                return "Esse número parece inválido. Pode me informar apenas os dígitos do seu telefone?"
            self.telefone = telefone_limpo
            self.estado = "aguardando_categoria"
            return "Obrigado! O que você está procurando hoje? Temos smartphones, laptops, smartwatches e mais."

        elif self.estado == "aguardando_categoria":
            produtos_relevantes = retrieve_products(msg)
            if produtos_relevantes:
                self.produto_sugerido = produtos_relevantes[0]["nome"]
                self.estado = "aguardando_preferencias"
                return f"Que bom saber que você está procurando um {self.produto_sugerido}. Tem alguma preferência em mente?"
            else:
                return self.gerar_resposta_gpt(mensagem)

        elif self.estado == "aguardando_preferencias" and self.aguardando_preferencia:
            self.aguardando_preferencia = False
            preco = next((p["preco"] for p in produtos_relevantes if p["nome"] == self.produto_sugerido), 0)
            descricao = next((p["descricao"] for p in produtos_relevantes if p["nome"] == self.produto_sugerido), "")
            self.estado = "pronto_para_fechar"
            return (f"Entendo. Recomendaria o {self.produto_sugerido}. {descricao} "
                    f"O preço dele é de R$ {preco:,.2f}. O que acha?")

        elif self.estado == "pronto_para_fechar":
            if "pagamento" in msg:
                return self.responder_pagamento()
            elif "garantia" in msg:
                return self.responder_garantia()

            fechar_palavras = [
                "sim", "quero", "fechar", "comprar", 
                "finalizar", "finalizar compra", "fechar pedido", "finalizar pedido"
            ]
            if any(palavra in msg for palavra in fechar_palavras):
                return self.gerar_proposta()

            return "Posso te ajudar com mais alguma coisa ou você gostaria de finalizar a compra?"

        return self.gerar_resposta_gpt(mensagem)

    def responder_pagamento(self):
        return ("Claro! Temos várias opções de pagamento disponíveis, "
                "incluindo parcelamento em até 12 vezes sem juros. "
                "Posso te ajudar com mais alguma coisa?")

    def responder_garantia(self):
        return ("Sim, oferecemos garantia estendida por um custo adicional. "
                "Posso te fornecer mais detalhes sobre isso.")

    def gerar_proposta(self):
        preco = next((p["preco"] for p in produtos_relevantes if p["nome"] == self.produto_sugerido), 0)
        proposta = (
            f"Proposta Comercial:\n\n"
            f"Cliente: {self.nome}\n"
            f"E-mail: {self.email}\n"
            f"Telefone: {self.telefone}\n\n"
            f"Produto: {self.produto_sugerido}\n"
            f"Preço: R$ {preco:,.2f}\n\n"
            f"Obrigado pela preferência! Vou te enviar o link para finalizar a compra agora mesmo. Link: www.uol.com.br\n\n"
            f"Se quiser conversar novamente, é só me mandar uma mensagem!"
        )
        self.estado = "inicial"
        self.nome = self.email = self.telefone = self.produto_sugerido = self.categoria_interesse = None
        self.aguardando_preferencia = False
        return proposta

    def gerar_resposta_gpt(self, mensagem):
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente de atendimento ao cliente para uma loja de tecnologia."},
                    {"role": "user", "content": mensagem}
                ],
                max_tokens=150,
                temperature=0.7
            )
            texto = resposta.choices[0].message.content.strip()
            print("✅ Resposta GPT:", texto)
            return texto
        except Exception as e:
            print("❌ Erro ao chamar a API GPT:", e)
            return "Desculpe, não consegui entender. Pode reformular sua pergunta?"
