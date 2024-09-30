import sqlite3

DATABASE = 'banco_de_dados.db'

def popular_bd():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Dados de exemplo
    produtos = [
        ("Bolo de Chocolate", "Bolo de chocolate com cobertura de brigadeiro", 29.99, "bolo", True),
        ("Bolo de Morango", "Bolo de morango com recheio de creme e cobertura de chantilly", 34.99, "bolo", True),
        ("Bolo de Cenoura", "Bolo de cenoura com cobertura de chocolate", 27.99, "bolo", True)
    ]
    
    cursor.executemany('''
        INSERT INTO produtos (nome, descricao, preco, categoria, disponivel)
        VALUES (?, ?, ?, ?, ?)
    ''', produtos)
    
    conn.commit()
    conn.close()
    print("Dados inseridos com sucesso.")

if __name__ == '__main__':
    popular_bd()
