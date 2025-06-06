import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from products import products, product_details, product_keywords

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
            self.email = mensagem.strip()
            self.estado = "aguardando_telefone"
            return "E o seu telefone?"

        elif self.estado == "aguardando_telefone":
            self.telefone = mensagem.strip()
            self.estado = "aguardando_categoria"
            return "Obrigado! O que você está procurando hoje? Temos smartphones, laptops, smartwatches e mais."

        elif self.estado == "aguardando_categoria":
            for produto, keywords in product_keywords.items():
                for kw in keywords:
                    if kw in msg:
                        self.categoria_interesse = kw
                        self.produto_sugerido = produto
                        self.estado = "aguardando_preferencias"
                        self.aguardando_preferencia = True
                        return f"Que bom saber que você está procurando um {kw}. Tem alguma preferência em mente?"
            return "Legal! Pode me dizer qual tipo de produto você está procurando? Por exemplo: smartphone, notebook, relógio, etc."

        elif self.estado == "aguardando_preferencias" and self.aguardando_preferencia:
            self.aguardando_preferencia = False
            preco = products.get(self.produto_sugerido)
            descricao = product_details.get(self.produto_sugerido)
            self.estado = "pronto_para_fechar"
            return (f"Entendo. Recomendaria o {self.produto_sugerido}. {descricao} "
                    f"O preço dele é de R$ {preco:,.2f}. O que acha?")

        elif self.estado == "pronto_para_fechar":
            if "pagamento" in msg:
                return "Claro! Temos várias opções de pagamento disponíveis, incluindo parcelamento em até 12 vezes sem juros. Posso te ajudar com mais alguma coisa?"
            elif "garantia" in msg:
                return "Sim, oferecemos garantia estendida por um custo adicional. Posso te fornecer mais detalhes sobre isso."

            fechar_palavras = ["sim", "quero", "fechar", "comprar", "finalizar", "finalizar compra", "fechar pedido", "finalizar pedido"]
            if any(palavra in msg for palavra in fechar_palavras):
                return self.gerar_proposta()

            return "Posso te ajudar com mais alguma coisa ou você gostaria de finalizar a compra?"

        # Fallback geral (usa GPT)
        return self.gerar_resposta_gpt(mensagem)

    def gerar_proposta(self):
        preco = products.get(self.produto_sugerido, 0)
        proposta = (
            f"Proposta Comercial:\n\n"
            f"Cliente: {self.nome}\n"
            f"E-mail: {self.email}\n"
            f"Telefone: {self.telefone}\n\n"
            f"Produto: {self.produto_sugerido}\n"
            f"Preço: R$ {preco:,.2f}\n\n"
            f"Obrigado pela preferência! Vou te enviar o link para finalizar a compra agora mesmo. Link: www.uol.com.br"
        )
        self.estado = "inicial"
        self.nome = self.email = self.telefone = self.produto_sugerido = self.categoria_interesse = None
        return proposta

    def gerar_resposta_gpt(self, mensagem):
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": mensagem}],
                max_tokens=150,
                temperature=0.7
            )
            return resposta.choices[0].message.content.strip()
        except Exception:
            return "Desculpe, não consegui entender. Pode reformular sua pergunta?"
