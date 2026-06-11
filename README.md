# Delivery API - FastAPI

Uma API REST desenvolvida com **FastAPI** para simular um sistema de delivery, aplicando boas práticas de desenvolvimento Back-end, autenticação de usuários, modelagem de banco de dados e arquitetura REST.

O projeto foi criado com tecnologias modernas do ecossistema Python e conceitos utilizados em aplicações reais.

---

## 👾 Tecnologias

* Python 3
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* JWT Authentication
* Passlib (Bcrypt)
* Python-JOSE
* Python-Dotenv
* Python-Multipart
* Pydantic

---

## 📋 Funcionalidades

### Usuários

* Cadastro de usuários;
* Login com autenticação JWT;
* Criptografia de senhas;
* Controle de permissões;
* Usuário administrador.

### Pedidos

* Criação de pedidos;
* Controle de status:

  * Pendente;
  * Cancelado;
  * Concluído;
* Associação entre usuários e pedidos.

### Itens do Pedido

* Adição de itens ao pedido;
* Quantidade;
* Sabor;
* Tamanho;
* Preço unitário.

---

## 🗄️ Modelagem do Banco de Dados

Atualmente o projeto possui três entidades principais:

### Usuários

| Campo | Tipo    |
| ----- | ------- |
| id    | Integer |
| nome  | String  |
| email | String  |
| senha | String  |
| ativo | Boolean |
| admin | Boolean |

---

### Pedidos

| Campo      | Tipo        |
| ---------- | ----------- |
| id         | Integer     |
| status     | Enum        |
| preco      | Float       |
| usuario_id | Foreign Key |

Status disponíveis:

* PENDENTE
* CANCELADO
* CONCLUIDO

---

### Itens do Pedido

| Campo          | Tipo        |
| -------------- | ----------- |
| id             | Integer     |
| quantidade     | Integer     |
| sabor          | String      |
| tamanho        | String      |
| preco_unitario | Float       |
| pedido_id      | Foreign Key |

---

## 🔗 Relacionamentos

```text
Usuário
   │
   ├── Pedido
   │      │
   │      ├── Item do Pedido
   │      ├── Item do Pedido
   │      └── Item do Pedido
```

Um usuário pode possuir vários pedidos.

Um pedido pode possuir vários itens.

Cada item pertence a um único pedido.

---
A estrutura foi organizada visando escalabilidade e manutenção do código.

---

## ⚙️ Instalação

Clone o projeto:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git

cd seu-projeto
```

Crie um ambiente virtual:

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração

Crie um arquivo `.env`:

```env
SECRET_KEY=sua_chave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL=sqlite:///banco.db
```

---

## ▶️ Executando a aplicação

```bash
uvicorn main:app --reload
```

Servidor:

```
http://127.0.0.1:8000
```

---

## 📖 Documentação

O FastAPI gera documentação automaticamente.

### Swagger

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 🔒 Autenticação

A API utiliza JWT (JSON Web Token).

Fluxo de autenticação:

1. Cadastro do usuário;
2. Login;
3. Geração do Access Token;
4. Acesso às rotas protegidas.

Exemplo:

```
Authorization: Bearer seu_token
```

---

## 🎯 Conceitos Aplicados

* REST API;
* CRUD;
* SQLAlchemy ORM;
* Modelagem de banco de dados;
* Relacionamentos entre tabelas;
* Autenticação JWT;
* Criptografia de senhas;
* Validação de dados com Pydantic;
* Variáveis de ambiente;
* Arquitetura em camadas;
* Boas práticas de desenvolvimento Back-end.

---

## 🚧 Melhorias Futuras

* Cadastro de produtos;
* Categorias;
* Carrinho de compras;
* Histórico de pedidos;
* Upload de imagens;
* Controle de estoque;
* Testes automatizados;
* Docker;
* Deploy em nuvem.

---

## 👨‍💻 Autor

**Felipe Duarte**

Projeto desenvolvido para práticas de desenvolvimento Back-end com FastAPI, SQLAlchemy e autenticação JWT, simulando um sistema de delivery com arquitetura escalável e boas práticas de desenvolvimento.
