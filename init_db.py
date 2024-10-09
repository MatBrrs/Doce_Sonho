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

def criar_tabela():
    # Criar todas as tabelas
    with app.app_context():
        db.create_all()  # Isso cria todas as tabelas definidas pelos modelos
        print("Tabela 'produtos' criada com sucesso.")

if __name__ == '__main__':
    criar_tabela()
