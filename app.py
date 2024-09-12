from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def inicializar_banco():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT,
                        preco REAL NOT NULL,
                        categoria TEXT NOT NULL,
                        disponivel BOOLEAN NOT NULL)''')
    cursor.executemany('''INSERT INTO produtos (nome, descricao, preco, categoria, disponivel)
                          VALUES (?, ?, ?, ?, ?)''', [
                              ("Bolo de Chocolate", "Bolo de chocolate com cobertura de brigadeiro", 29.99, "bolo", True),
                              ("Bolo de Morango", "Bolo de morango com recheio de creme e cobertura de chantilly", 34.99, "bolo", True),
                              ("Bolo de Cenoura", "Bolo de cenoura com cobertura de chocolate", 27.99, "bolo", True)
                          ])
    conn.commit()
    return conn

conn = inicializar_banco()

@app.route('/v1/produtos', methods=['GET'])
def listar_produtos():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    lista_produtos = [{"id": row[0], "nome": row[1], "descricao": row[2], "preco": row[3], "categoria": row[4], "disponivel": row[5]} for row in produtos]
    return jsonify(lista_produtos), 200

@app.route('/v1/produtos', methods=['POST'])
def adicionar_produto():
    novo_produto = request.json
    if not novo_produto.get('nome') or not novo_produto.get('preco') or not novo_produto.get('categoria'):
        return jsonify({"error": "Campos obrigatórios: nome, preco, categoria"}), 400

    cursor = conn.cursor()
    cursor.execute('''INSERT INTO produtos (nome, descricao, preco, categoria, disponivel)
                      VALUES (?, ?, ?, ?, ?)''', 
                   (novo_produto['nome'], novo_produto.get('descricao'), novo_produto['preco'], novo_produto['categoria'], novo_produto.get('disponivel', True)))
    conn.commit()
    novo_produto['id'] = cursor.lastrowid
    return jsonify(novo_produto), 201

@app.route('/v1/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if produto:
        produto_dict = {"id": produto[0], "nome": produto[1], "descricao": produto[2], "preco": produto[3], "categoria": produto[4], "disponivel": produto[5]}
        return jsonify(produto_dict), 200
    return jsonify({"error": "Produto não encontrado"}), 404

@app.route('/v1/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    dados_atualizados = request.json
    cursor.execute('''UPDATE produtos
                      SET nome = ?, descricao = ?, preco = ?, categoria = ?, disponivel = ?
                      WHERE id = ?''', 
                   (dados_atualizados.get('nome', produto[1]),
                    dados_atualizados.get('descricao', produto[2]),
                    dados_atualizados.get('preco', produto[3]),
                    dados_atualizados.get('categoria', produto[4]),
                    dados_atualizados.get('disponivel', produto[5]),
                    produto_id))
    conn.commit()
    return jsonify({"id": produto_id, **dados_atualizados}), 200

@app.route('/v1/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404
    
    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
