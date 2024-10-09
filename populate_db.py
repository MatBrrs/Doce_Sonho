from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuração do aplicativo Flask e do banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_de_dados.db'
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

# Função para popular o banco de dados
def popular_bd():
    # Criar todas as tabelas
    with app.app_context():
        db.create_all()  # Certifique-se de que as tabelas estão criadas

        # Dados de exemplo
        produtos = [
            Produto(nome="Bolo de Chocolate", descricao="Bolo de chocolate com cobertura de brigadeiro", preco=29.99, categoria="bolo", disponivel=True),
            Produto(nome="Bolo de Morango", descricao="Bolo de morango com recheio de creme e cobertura de chantilly", preco=34.99, categoria="bolo", disponivel=True),
            Produto(nome="Bolo de Cenoura", descricao="Bolo de cenoura com cobertura de chocolate", preco=27.99, categoria="bolo", disponivel=True)
        ]
        
        # Adicionando os produtos ao banco de dados
        db.session.add_all(produtos)
        db.session.commit()
        print("Dados inseridos com sucesso.")

if __name__ == '__main__':
    popular_bd()
