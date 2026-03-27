## 📦 API MaxFit

A API MaxFit é uma aplicação REST desenvolvida em Python com Flask, voltada para o gerenciamento de produtos de uma loja de suplementos fictícia.

O projeto permite realizar operações básicas de CRUD em produtos, com integração a banco de dados MySQL, cujo modelo e estrutura foram desenvolvidos por mim, incluindo definição de tabelas, relacionamentos e constraints.

### ⚙️ Funcionalidades
- Listagem de produtos (GET /produtos)
- Cadastro de novos produtos (POST /produtos)
- Validação de dados de entrada
- Integração com banco de dados relacional (MySQL)

### 🧪 Testes
- Testes de requisições utilizando Postman
- Validação de respostas e códigos de status HTTP

### 🛠️ Tecnologias utilizadas
- Python
- Flask
- MySQL
- Postman

### 🎯 Objetivo
O objetivo do projeto é praticar o desenvolvimento de APIs REST, modelagem de banco de dados e testes de API, consolidando conhecimentos em backend e QA.

### 🚀 Próximos passos
- Implementar rotas de atualização (PUT), exclusão (DELETE) para produtos e finalizar todas as rotas para categoria.
- Adicionar filtros e paginação
- Realizar deploy da aplicação

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## ▶️ Como executar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/artmac1233/Max-Fit-API.git
cd Max-Fit-API

### 2. Criar ambiente virtual (opcional, mas recomendado)
# 2.1. Criar ambiente virtual
python -m venv venv

# 2.2. Ativar o ambiente
venv\Scripts\activate

### 3. Instalar dependências
pip install -r requirements.txt

### 4. Configurar variáveis de ambiente
Crie um arquivo .env na raiz do projeto com suas credenciais do banco de dados:

DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=maxfit

### 6. Importar o banco de dados
Abra o MySQL no terminal ou no Workbench e execute:
CREATE DATABASE maxfit;

Execute o seguinte comando no terminal, dentro da pasta do projeto:
mysql -u root -p maxfit < database/schema.sql

O projeto já contém o arquivo schema.sql com toda a estrutura do banco na pasta Database

### 5. Executar a aplicação
python app.py

A API estará disponível em: http://127.0.0.1:5000
