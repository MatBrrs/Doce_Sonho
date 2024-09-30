from fastapi.testclient import TestClient
from main import app

# Cria um cliente de testes usando a aplicação FastAPI
client = TestClient(app)

def test_criar_sonho():
    response = client.post("/sonhos/", json={"titulo": "Sonho 1", "descricao": "Descrição do Sonho 1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Sonho criado com sucesso!"}

def test_listar_sonhos():
    # Certifique-se de que há pelo menos um sonho criado antes de executar este teste
    response = client.get("/sonhos/")
    assert response.status_code == 200
    assert "sonhos" in response.json()
    assert len(response.json()["sonhos"]) > 0  # Verifica se há pelo menos um sonho listado

def test_obter_sonho():
    # Certifique-se de que há pelo menos um sonho com ID 1
    response = client.get("/sonhos/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 1
    assert "titulo" in data
    assert "descricao" in data

def test_sonho_nao_encontrado():
    response = client.get("/sonhos/9999")  # Tenta acessar um ID inexistente
    assert response.status_code == 404
    assert response.json() == {"detail": "Sonho não encontrado"}

def test_deletar_sonho():
    # Certifique-se de que há um sonho com ID 1
    response = client.delete("/sonhos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Sonho deletado com sucesso!"}
    
    # Verifica se o sonho foi realmente deletado
    response = client.get("/sonhos/1")
    assert response.status_code == 404
