from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'banco_de_dados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=(), fetchone=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetchone:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

@app.route('/v1/produtos', methods=['GET'])
def listar_produtos():
    try:
        produtos = execute_query('SELECT * FROM produtos')
        return jsonify([dict(row) for row in produtos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos', methods=['POST'])
def adicionar_produto():
    try:
        novo_produto = request.json
        if not novo_produto.get('nome') or not novo_produto.get('preco') or not novo_produto.get('categoria'):
            return jsonify({"error": "Campos obrigatórios: nome, preco, categoria"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, preco, categoria, disponivel)
            VALUES (?, ?, ?, ?, ?)
        ''', (novo_produto['nome'], novo_produto.get('descricao', ''), novo_produto['preco'], novo_produto['categoria'], novo_produto.get('disponivel', True)))
        conn.commit()
        
        # Obter o ID recém-criado
        novo_produto['id'] = cursor.lastrowid
        conn.close()
        
        return jsonify(novo_produto), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    try:
        produto = execute_query('SELECT * FROM produtos WHERE id = ?', (produto_id,), fetchone=True)
        if produto:
            return jsonify(dict(produto)), 200
        return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    try:
        dados_atualizados = request.json
        execute_query('''
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, categoria = ?, disponivel = ?
            WHERE id = ?
        ''', (dados_atualizados['nome'], dados_atualizados.get('descricao', ''), dados_atualizados['preco'], dados_atualizados['categoria'], dados_atualizados.get('disponivel', True), produto_id))
        
        return jsonify(dados_atualizados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        conn.close()
        
        if cursor.rowcount > 0:
            return '', 204
        else:
            return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)