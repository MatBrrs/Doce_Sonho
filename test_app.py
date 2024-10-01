import pytest
from app import app  # Certifique-se de que o nome do seu arquivo Flask seja 'app.py'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_adicionar_produto(client):
    response = client.post('/v1/produtos', json={
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto teste',
        'preco': 10.0,
        'categoria': 'Categoria Teste',
        'disponivel': True
    })
    assert response.status_code == 201
    assert 'id' in response.json  # Verifica se o 'id' está presente na resposta

def test_listar_produtos(client):
    response = client.get('/v1/produtos')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Verifica se o retorno é uma lista

def test_obter_produto(client):
    response = client.post('/v1/produtos', json={
        'nome': 'Produto para obter',
        'descricao': 'Descrição do produto',
        'preco': 15.0,
        'categoria': 'Categoria',
        'disponivel': True
    })
    produto_id = response.json['id']
    
    response = client.get(f'/v1/produtos/{produto_id}')
    assert response.status_code == 200
    assert response.json['id'] == produto_id

def test_deletar_produto(client):
    response = client.post('/v1/produtos', json={
        'nome': 'Produto para deletar',
        'descricao': 'Descrição do produto',
        'preco': 20.0,
        'categoria': 'Categoria',
        'disponivel': True
    })
    produto_id = response.json['id']
    
    response = client.delete(f'/v1/produtos/{produto_id}')
    assert response.status_code == 204

    response = client.get(f'/v1/produtos/{produto_id}')
    assert response.status_code == 404
