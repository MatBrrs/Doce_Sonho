import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Verifique se está em teste para usar um banco de dados em memória
if os.getenv('TESTING'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Para testes
else:
    # Configure a conexão com um banco de dados PostgreSQL remoto
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mysql+pymysql://mateus:Qe#Xv}ql2?L37ibp@34.79.51.239:3306/mateus_schema"
    )  # Substitua pelos detalhes do seu banco de dados

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição do modelo de produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

# Criar todas as tabelas
with app.app_context():
    db.create_all()

@app.route('/v1/produtos', methods=['GET'])
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return jsonify([produto_to_dict(produto) for produto in produtos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos', methods=['POST'])
def adicionar_produto():
    try:
        novo_produto = request.json
        if not novo_produto.get('nome') or not novo_produto.get('preco') or not novo_produto.get('categoria'):
            return jsonify({"error": "Campos obrigatórios: nome, preco, categoria"}), 400

        produto = Produto(
            nome=novo_produto['nome'],
            descricao=novo_produto.get('descricao', ''),
            preco=novo_produto['preco'],
            categoria=novo_produto['categoria'],
            disponivel=novo_produto.get('disponivel', True)
        )
        db.session.add(produto)
        db.session.commit()
        
        return jsonify(produto_to_dict(produto)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if produto:
            return jsonify(produto_to_dict(produto)), 200
        return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    try:
        dados_atualizados = request.json
        produto = Produto.query.get(produto_id)

        if produto:
            produto.nome = dados_atualizados['nome']
            produto.descricao = dados_atualizados.get('descricao', '')
            produto.preco = dados_atualizados['preco']
            produto.categoria = dados_atualizados['categoria']
            produto.disponivel = dados_atualizados.get('disponivel', True)
            
            db.session.commit()

            return jsonify(produto_to_dict(produto)), 200
        return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    try:
        produto = Produto.query.get(produto_id)
        if produto:
            db.session.delete(produto)
            db.session.commit()
            return '', 204
        return jsonify({"error": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/produtos/categoria/<string:categoria>', methods=['GET'])
def buscar_por_categoria(categoria):
    try:
        produtos = Produto.query.filter_by(categoria=categoria).all()
        return jsonify([produto_to_dict(produto) for produto in produtos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Função auxiliar para converter o objeto Produto em dicionário
def produto_to_dict(produto):
    return {
        'id': produto.id,
        'nome': produto.nome,
        'descricao': produto.descricao,
        'preco': produto.preco,
        'categoria': produto.categoria,
        'disponivel': produto.disponivel
    }

if __name__ == '__main__':
    app.run(debug=True)
