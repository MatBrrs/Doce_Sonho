import SQLAlchemy

DATABASE = 'banco_de_dados.db'

def criar_tabela():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            categoria TEXT NOT NULL,
            disponivel BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabela()
    print("Tabela 'produtos' criada com sucesso.")
