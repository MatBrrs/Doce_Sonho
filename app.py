
# Rota para listar todos os produtos
@app.route('/v1/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return jsonify([dict(produto) for produto in produtos]), 200

# Rota para adicionar um novo produto
@app.route('/v1/produtos', methods=['POST'])
def adicionar_produto():
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
    conn.close()
    return jsonify(novo_produto), 201

# Rota para obter um produto por ID
@app.route('/v1/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    if produto:
        return jsonify(dict(produto)), 200
    return jsonify({"error": "Produto não encontrado"}), 404

# Rota para atualizar um produto existente
@app.route('/v1/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    dados_atualizados = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        conn.close()
        return jsonify({"error": "Produto não encontrado"}), 404

    cursor.execute('''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, categoria = ?, disponivel = ?
        WHERE id = ?
    ''', (dados_atualizados.get('nome', produto['nome']),
          dados_atualizados.get('descricao', produto['descricao']),
          dados_atualizados.get('preco', produto['preco']),
          dados_atualizados.get('categoria', produto['categoria']),
          dados_atualizados.get('disponivel', produto['disponivel']),
          produto_id))
    conn.commit()
    conn.close()
    return jsonify(dict(produto)), 200

# Rota para deletar um produto
@app.route('/v1/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        conn.close()
        return jsonify({"error": "Produto não encontrado"}), 404

    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
