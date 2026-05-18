import sqlite3
import logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
def conectar():
    return sqlite3.connect("finance.db")
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            valor REAL,              
            descricao TEXT,
            categoria TEXT,
            tipo TEXT
        )
  ''')
    
    conn.commit()
    conn.close()
def salvar_transacao(data, valor, descricao, categoria, tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO transacoes (data, valor, descricao, categoria, tipo)
        VALUES (?, ?, ?, ?, ?)
    ''', (data, valor, descricao, categoria, tipo))
    
    conn.commit()
    conn.close()
    logging.info(f"Transação salva: {descricao} - R${valor} - {tipo}")
def buscar_transacoes_mes(mes, ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM transacoes
        WHERE strftime('%m', data) = ?
        AND strftime('%Y', data) = ?
    ''', (str(mes).zfill(2), str(ano))
    
    )

    transacoes = cursor.fetchall()
    conn.close()
    return transacoes
def buscar_por_categoria(categoria, mes, ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * from transacoes
        WHERE categoria = ?
        AND strftime('%m', data) = ?
        AND strftime('%Y', data) = ?
    ''', (str(categoria), str(mes).zfill(2), str(ano))

 
    )

    transacoes = cursor.fetchall()
    conn.close()
    return transacoes
def calcular_saldo(mes, ano):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(valor) FROM transacoes
        WHERE tipo = 'receita'
        AND strftime('%m', data) = ?
        AND strftime('%Y', data) = ?
    ''', (str(mes).zfill(2), str(ano))                              

    )
    
    receita = cursor.fetchone()[0] or 0

    cursor.execute('''
        SELECT SUM(valor) FROM transacoes
        WHERE tipo = 'gasto'
        AND strftime('%m', data) = ?
        AND strftime('%Y', data) = ?
    ''', (str(mes).zfill(2), str(ano))


    )

    gasto = cursor.fetchone()[0] or 0

    conn.close()
    return receita - gasto

def resumo_por_categoria(mes, ano):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT categoria, SUM(valor) FROM transacoes
    WHERE strftime('%m', data) = ? 
    AND strftime('%Y', data) = ?
    GROUP BY categoria
''', (str(mes).zfill(2), str(ano))

    )
    
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes
def deletar_transacao(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM transacoes WHERE id = ?
''', (id,))
    
    
    conn.commit()
    conn.close()

 