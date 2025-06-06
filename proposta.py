def gerar_proposta(nome, email, telefone, produto, preco):
    return f"""
📄 Proposta Comercial

Cliente: {nome}
E-mail: {email}
Telefone: {telefone}

Produto: {produto}
Preço: R$ {preco:,.2f}

Condições:
- Parcelamento em até 12x sem juros
- Garantia padrão de 12 meses
"""
