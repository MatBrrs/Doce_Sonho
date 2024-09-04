# 🍰 Doce Sonho - API de Catálogo de Bolos e Doces

**API para gerenciar o catálogo de produtos de uma loja de bolos e doces.**

## 📖 Índice
- [Visão Geral](#visão-geral)
- [Recursos da API](#recursos-da-api)
- [Instalação e Execução](#instalação-e-execução)
- [Exemplos de Uso](#exemplos-de-uso)
- [Esquemas de Dados](#esquemas-de-dados)
- [Autores](#autores)

## 📝 Visão Geral

A **Loja de Bolos e Doces API** é um serviço RESTful que permite gerenciar o catálogo de produtos de uma loja de bolos e doces, incluindo operações como listar, adicionar, atualizar e excluir produtos.

### 🌐 URL Base

A API está disponível em dois ambientes:

- **Mock Server**: [https://virtserver.swaggerhub.com/MATEUS1BARROS5/Doce_Sonho/1.0.0](https://virtserver.swaggerhub.com/MATEUS1BARROS5/Doce_Sonho/1.0.0)
- **Servidor Local**: `http://localhost:8080/v1`

## 🚀 Recursos da API

### 1. Listar Produtos

- **Descrição**: Retorna uma lista de todos os produtos disponíveis.
- **Endpoint**: `GET /produtos`
- **Resposta**:
  - `200 OK`: Lista de produtos retornada com sucesso.

---

### 2. Adicionar Produto

- **Descrição**: Adiciona um novo produto ao catálogo.
- **Endpoint**: `POST /produtos`
- **Corpo da Requisição**:

```json
{
  "nome": "Bolo de Cenoura",
  "descricao": "Bolo de cenoura com cobertura de chocolate",
  "preco": 27.99,
  "categoria": "bolo",
  "disponivel": true
}
