import imaplib
import email
import re
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

def conectar_email(usuario, senha):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(usuario, senha)
    return mail
def ler_emails_inter(mail, completo=False):
    mail.select("inbox")
    _, ids = mail.search(None, 'FROM', '"no-reply@inter.co"')
    todos = ids[0].split()
    return todos if completo else todos [-10:]
def extrair_dados_email(msg):
    corpo = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/plain", "text/html"):
                corpo = part.get_payload(decode=True).decode()
                break
    else:
        corpo = msg.get_payload(decode=True).decode()

    print(corpo)

    valor = re.search(r'R\$\s*R\$\s*([\d.,]+)', corpo)
    data = re.search(r'(\d{2}/\d{2}/\d{4})', corpo)
    descricao = re.search(r'Nome:\s*([^<\n]+)', corpo)
    print(f"valor={valor}, data={data}, descricao={descricao}")

    return { 
        "valor": float(valor.group(1).replace(".", "").replace(",", ".")) if valor else 0,
        "data": data.group(1) if data else "",
        "descricao": descricao.group(1).strip() if descricao else ""
    }
        
def processar_emails(usuario, senha, completo=False):
    try:
        mail = conectar_email(usuario, senha)
        ids = ler_emails_inter(mail, completo)
        transacoes = []
        for id in ids:
            _, msg_data = mail.fetch(id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            dados = extrair_dados_email(msg)
            if dados["valor"] > 0:
                transacoes.append(dados)
        mail.logout()
        return transacoes
    except Exception as e:
        print(f"ERRO: {e}")
        return []
