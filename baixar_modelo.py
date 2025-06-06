from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("Modelo e tokenizer carregados com sucesso!")
