import os
from dotenv import load_dotenv

load_dotenv()

chave = os.getenv("OPENAI_API_KEY")
if chave:
    print("✅ Variável OPENAI_API_KEY foi carregada com sucesso!")
    print("Valor (ocultado):", chave[:8] + "..." + chave[-4:])
else:
    print("❌ Variável OPENAI_API_KEY **não** foi carregada.")
