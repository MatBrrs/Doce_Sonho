# Doce_Sonho
Api direcionada a catalogos de bolo
Loja de Bolos e Doces API
API para gerenciar o catálogo de produtos de uma loja de bolos e doces.

Índice
 Visão Geral
 Recursos da API
 Instalação e Execução
 Exemplos de Uso
 Esquemas de Dados
 Autores

Visão Geral
 A Loja de Bolos e Doces API é um serviço que permite gerenciar o catálogo de produtos de uma loja, incluindo operações para listar, 
 adicionar, atualizar e excluir produtos como bolos e doces.

URL Base
 A API está disponível em dois ambientes:
  Mock Server: https://virtserver.swaggerhub.com/MATEUS1BARROS5/Doce_Sonho/1.0.0
  Servidor local: http://localhost:8080/v1

Recursos da API
 Listar Produtos
  Descrição: Retorna uma lista de todos os produtos disponíveis.
  Endpoint: GET /produtos
 Resposta:
  200 OK: Retorna uma lista de produtos.

Adicionar Produto
 Descrição: Adiciona um novo produto ao catálogo.
 Endpoint: POST /produtos
 Corpo da Requisição:
  json
   {
     "nome": "Bolo de Cenoura",
     "descricao": "Bolo de cenoura com cobertura de chocolate",
     "preco": 27.99,
     "categoria": "bolo",
     "disponivel": true
   }
 Resposta:
  201 Created: Retorna o produto criado.

Obter Produto pelo ID
 Descrição: Retorna detalhes de um produto específico usando seu ID.
 Endpoint: GET /produtos/{id}
 Parâmetros:
  id (string): ID do produto.
 Resposta:
  200 OK: Retorna o produto solicitado.
  404 Not Found: Produto não encontrado.

Atualizar Produto
 Descrição: Atualiza os detalhes de um produto existente.
 Endpoint: PUT /produtos/{id}
 Parâmetros:
  id (string): ID do produto.
 Corpo da Requisição:
  json
   {
     "nome": "Bolo de Chocolate",
     "descricao": "Bolo de chocolate com cobertura de brigadeiro",
     "preco": 29.99,
     "categoria": "bolo",
     "disponivel": true
   }
 Resposta:
  200 OK: Produto atualizado com sucesso.
  404 Not Found: Produto não encontrado.

Deletar Produto
 Descrição: Remove um produto do catálogo usando seu ID.
 Endpoint: DELETE /produtos/{id}
 Parâmetros:
  id (string): ID do produto.
 Resposta:
  204 No Content: Produto deletado com sucesso.
  404 Not Found: Produto não encontrado.

Instalação e Execução
 1. Clone o repositório:
  git clone https://github.com/seu-usuario/loja-de-bolos-e-doces-api.git
  cd loja-de-bolos-e-doces-api
 2. Instale as dependências:
  npm install
 3. Execute o servidor localmente:
  npm start
 4. Acesse a API no servidor local em: http://localhost:8080/v1.

Exemplos de Uso
 cURL:
  Listar produtos:
   curl -X GET "http://localhost:8080/v1/produtos" -H "accept: application/json"
  Adicionar um novo produto:
   curl -X POST "http://localhost:8080/v1/produtos" -H "Content-Type: application/json" -d '{
    "nome": "Bolo de Cenoura",
    "descricao": "Bolo de cenoura com cobertura de chocolate",
    "preco": 27.99,
    "categoria": "bolo",
    "disponivel": true
   }'

Esquemas de Dados
Produto
Campo	          Tipo	           Descrição
 id	             string	        ID único do produto
 nome	           string	        Nome do produto
 descricao       string 	      Descrição do produto
 preco	         number	        Preço do produto
 categoria	     string	        Categoria do produto (ex.: bolo, doce)
 disponivel	     boolean	      Indica se o produto está disponível

Autores
 Matheus Barros - MatBrrs
