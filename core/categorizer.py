def categorizar(descricao):
    descricao = descricao.lower()
    palavras = ["ifood", "restaurante", "comida", "lanche", "aiqfome", "salgado", "salgados"]
    if any (p in descricao for p in palavras):
        return "Alimentação"
    palavras = ["remédio", "farmácia", "médico", "hospital", "cuidado"]
    if any (p in descricao for p in palavras):
        return "Saúde"
    palavras = ["salario", "salário", "pagamento"]
    if any (p in descricao for p in palavras):
        return "Salário"
    palavras = ["freela", "freelancer", "serviço"]
    if any (p in descricao for p in palavras):
        return "Freela"
    return "Outros"