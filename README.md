# 🐾 Sistema de Gestão para Pet Shop (V2.0) – Python CLI + MySQL

Este projeto é um **sistema de gestão para pet shop**, desenvolvido em **Python (modo CLI)** com integração ao **MySQL**.  
O objetivo é oferecer um sistema simples, modularizado e bem estruturado para:

- Gerenciar **clientes e pets**
- Cadastrar **serviços e produtos**
- Controlar **agendamentos**
- Registrar **vendas**
- Gerenciar **usuários do sistema**

Além disso, o projeto foi pensado como **portfólio**, aplicando boas práticas de organização, persistência de dados e uso de variáveis de ambiente para credenciais.

---

## 🧰 Tecnologias utilizadas

- **Python 3.13** (ou 3.x)
- **MySQL**
- **python-dotenv** (variáveis de ambiente)
- **mysql-connector-python** (ou biblioteca similar para conexão com MySQL)
- Conceitos:
  - Arquitetura modular
  - CRUD (Create, Read, Update, Delete)
  - Separação de camadas (config, banco, regras de negócio, menus)

---

## 📁 Estrutura do projeto (resumo)

```text
Projeto_PetShop/
├── .env                 # Variáveis de ambiente (NÃO vai para o GitHub)
├── .gitignore
├── auth.py              # Autenticação de usuários
├── config.py            # Configurações (carrega o .env)
├── crud_agendamentos.py # CRUD de agendamentos
├── crud_clientes.py     # CRUD de clientes
├── crud_produtos.py     # CRUD de produtos
├── crud_servicos.py     # CRUD de serviços
├── crud_usuarios.py     # CRUD de usuários
├── crud_vendas.py       # CRUD de vendas
├── database.py          # Conexão com o MySQL
├── main.py              # Ponto de entrada do sistema (menu principal)
├── menus.py             # Menus da aplicação (CLI)
├── notifications.py     # Notificações (e-mail / Telegram, se configurado)
└── utils.py             # Funções utilitárias

dados_petshop/
└── Bancos de dados do Sistema.sql  # Script para criação das tabelas no MySQL

🗄️ Banco de dados

O arquivo:

dados_petshop/Bancos de dados do Sistema.sql


contém o script SQL para:

Criar o banco de dados meu_querido_pet

Criar as tabelas:

produtos

servicos

clientes

usuarios

agendamentos

vendas

Antes de rodar o sistema, importe esse arquivo no MySQL (via MySQL Workbench, DBeaver, CLI, etc).

🔐 Variáveis de ambiente (.env)

As credenciais e configurações sensíveis não ficam no código, e sim no arquivo .env (que é ignorado pelo Git).

Exemplo de .env:

PASTA_DADOS=dados_petshop

EMAIL_REMETENTE=seu_email@gmail.com
SENHA_APP_REMETENTE=sua_senha_de_app

BOT_TOKEN=seu_token_do_bot
CHAT_ID=seu_chat_id

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha_mysql
MYSQL_DB=meu_querido_pet


⚠️ O arquivo .env NÃO deve ser versionado.
O .gitignore já está configurado para ignorá-lo.

📦 Dependências

Crie um arquivo requirements.txt (se ainda não existir) com algo parecido com:

python-dotenv
mysql-connector-python


Para instalar as dependências:

pip install -r requirements.txt

▶️ Como executar o projeto

Clone o repositório:

git clone https://github.com/wanders0nlucian0/Sistema-de-Gest-o-para-Pet-Shop-V2.0-em-Python-CLI-com-MySQL.git
cd Sistema-de-Gest-o-para-Pet-Shop-V2.0-em-Python-CLI-com-MySQL/Projeto_PetShop


(Opcional, mas recomendado) Crie um ambiente virtual:

python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate  # Linux/Mac


Instale as dependências:

pip install -r requirements.txt


Configure o banco de dados:

Importe o arquivo dados_petshop/Bancos de dados do Sistema.sql no seu MySQL.

Crie o arquivo .env na pasta Projeto_PetShop com suas configurações.

Execute o sistema:

python main.py

✨ Funcionalidades (resumo)

👥 Clientes e Pets

Cadastro, listagem, atualização e exclusão

🛁 Serviços

Cadastro de serviços (banho, tosa, consultas, etc.)

🧴 Produtos

Controle de estoque e preços

📅 Agendamentos

Registrar, listar e atualizar agendamentos

💰 Vendas

Registro de vendas de produtos/serviços

🔐 Usuários

Controle de usuários do sistema

📢 Notificações (opcional)

Integração com e-mail e bot do Telegram (se configurado no .env)

🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

Praticar Python aplicado a sistemas reais

Usar MySQL com conexão via código

Aplicar boas práticas:

Separação de responsabilidades (módulos, CRUDs, config, DB)

Uso de variáveis de ambiente para dados sensíveis

Organização de projeto para portfólio

📜 Licença

Este projeto está licenciado sob a licença MIT.
Sinta-se à vontade para usar, modificar e estudar o código, mantendo os devidos créditos.
