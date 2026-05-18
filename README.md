# Finance App

Aplicativo de controle financeiro pessoal que importa transações automaticamente via email do Inter.

## Funcionalidades

- Dashboard com receitas, gastos e gráficos do mês
- Importação automática de transações via email do Inter
- Cadastro manual de transações
- Deletar transações
- Relatórios mensais com comparativo dos últimos 3 meses

## Requisitos

- Python 3.10+
- Conta Gmail com IMAP ativado
- Senha de App do Gmail (não a senha normal)

## Instalação

1. Clone o repositório:
```
git clone URL_DO_REPO
cd FinanceApp
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Crie o arquivo `.env` na raiz do projeto:
```
EMAIL=seu_email@gmail.com
SENHA=sua_senha_de_app
```

4. Como gerar a senha de app do Gmail:
   - Acesse myaccount.google.com
   - Segurança → Verificação em duas etapas (ative se não tiver)
   - Segurança → Senhas de app
   - Gere uma senha para "Email" e cole no `.env`

## Como rodar

```
python main.py
```

## Observações

- O botão **Atualizar** importa os 10 emails mais recentes do Inter
- O botão **Busca Completa** importa todos os emails do Inter
- O arquivo `.env` nunca deve ser compartilhado ou commitado
- O banco de dados `finance.db` é criado automaticamente na primeira execução

## Status

v1.0-alpha — base funcional, front em desenvolvimento