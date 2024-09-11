from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de produtos (mock data)
produtos = [
    {"id": "12345", "nome": "Bolo de Chocolate", "descricao": "Bolo de chocolate com cobertura de brigadeiro", "preco": 29.99, "categoria": "bolo", "disponivel": True},
    {"id": "12346", "nome": "Bolo de Morango", "descricao": "Bolo de morango com recheio de creme e cobertura de chantilly", "preco": 34.99, "categoria": "bolo", "disponivel": True},
    {"id": "12347", "nome": "Bolo de Cenoura", "descricao": "Bolo de cenoura com cobertura de chocolate", "preco": 27.99, "categoria": "bolo", "disponivel": True}
]

# Função auxiliar para encontrar um produto por ID
def encontrar_produto_por_id(produto_id):
    return next((produto for produto in produtos if produto['id'] == produto_id), None)

# Rota para listar todos os produtos
@app.route('/v1/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos), 200

# Rota para adicionar um novo produto
@app.route('/v1/produtos', methods=['POST'])
def adicionar_produto():
    novo_produto = request.json
    if not novo_produto.get('nome') or not novo_produto.get('preco') or not novo_produto.get('categoria'):
        return jsonify({"error": "Campos obrigatórios: nome, preco, categoria"}), 400
    
    novo_produto['id'] = str(len(produtos) + 12345)  # Simula um ID único
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# Rota para obter um produto por ID
@app.route('/v1/produtos/<string:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = encontrar_produto_por_id(produto_id)
    if produto:
        return jsonify(produto), 200
    return jsonify({"error": "Produto não encontrado"}), 404

# Rota para atualizar um produto existente
@app.route('/v1/produtos/<string:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    produto = encontrar_produto_por_id(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    dados_atualizados = request.json
    produto.update(dados_atualizados)
    return jsonify(produto), 200

# Rota para deletar um produto
@app.route('/v1/produtos/<string:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produto = encontrar_produto_por_id(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404
    
    produtos.remove(produto)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
