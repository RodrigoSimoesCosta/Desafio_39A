# create_faiss_index.py
import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
from product_data import product_data

# Carregar a chave da API do OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para gerar embeddings
def get_embedding(text):
    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Gerar embeddings para os nomes dos produtos
product_names = [product["nome"] for product in product_data]
product_embeddings = np.array([get_embedding(name) for name in product_names]).astype('float32')

# Criar o índice FAISS
dimension = product_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(product_embeddings)

# Salvar o índice FAISS
faiss.write_index(index, "product_index.faiss")

# Salvar os dados dos produtos
with open("product_data.npy", "wb") as f:
    np.save(f, product_data)
