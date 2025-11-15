# 🐾 Sistema de Gestão Meu Querido Pet (V2.0)

Este é um sistema completo de gerenciamento para Pet Shops, desenvolvido em Python como um aplicativo de console (CLI). O projeto foi totalmente refatorado da V1.0 para uma arquitetura modular, separando todas as responsabilidades em módulos independentes.

O sistema se conecta a um banco de dados **MySQL** e gerencia o CRUD completo de:
* Produtos (com controle de estoque)
* Clientes
* Serviços
* Agendamentos
* Vendas
* Usuários (com perfis de Admin e User)

## ✨ Principais Recursos (V2.0)

* **Autenticação:** Sistema de login seguro com hashing de senhas e dois níveis de permissão (Admin/User).
* **Integrações Externas:**
    * **Telegram:** Envio de notificações em tempo real para um chat via Bot (novas vendas, agendamentos, estoque baixo).
    * **SMTP (Gmail):** Envio de e-mails para recuperação de senha e boas-vindas a novos usuários.
* **Relatórios:** Geração de relatórios de vendas e estoque, com exportação direta para planilhas **Excel (.xlsx)**.
