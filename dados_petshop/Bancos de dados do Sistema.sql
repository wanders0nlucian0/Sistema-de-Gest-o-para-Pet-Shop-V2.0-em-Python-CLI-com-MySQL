-- Cria o banco de dados
CREATE DATABASE IF NOT EXISTS meu_querido_pet
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE meu_querido_pet;

-- ==========================
-- TABELA: produtos
-- ==========================
CREATE TABLE IF NOT EXISTS produtos (
    codigo     INT          NOT NULL PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    quantidade INT          NOT NULL,
    preco      DECIMAL(10,2) NOT NULL,
    validade   VARCHAR(10)   -- formato DD/MM/AAAA
);

-- ==========================
-- TABELA: servicos
-- ==========================
CREATE TABLE IF NOT EXISTS servicos (
    codigo     INT           NOT NULL PRIMARY KEY,
    nome       VARCHAR(100)  NOT NULL,
    descricao  TEXT,
    preco      DECIMAL(10,2) NOT NULL
);

-- ==========================
-- TABELA: clientes
-- ==========================
CREATE TABLE IF NOT EXISTS clientes (
    codigo   INT          NOT NULL PRIMARY KEY,
    tutor    VARCHAR(100) NOT NULL,
    pet      VARCHAR(100) NOT NULL,
    raca     VARCHAR(100) NOT NULL,
    servico  VARCHAR(100) -- nome do serviço
);

-- ==========================
-- TABELA: usuarios
-- ==========================
CREATE TABLE IF NOT EXISTS usuarios (
    usuario VARCHAR(50)   NOT NULL PRIMARY KEY,
    senha   VARCHAR(64)   NOT NULL, -- hash SHA-256 em hex
    perfil  VARCHAR(10)   NOT NULL, -- 'admin' ou 'user'
    email   VARCHAR(255)  NOT NULL UNIQUE
);

-- ==========================
-- TABELA: agendamentos
-- ==========================
CREATE TABLE IF NOT EXISTS agendamentos (
    codigo         INT          NOT NULL PRIMARY KEY,
    cliente_codigo INT          NOT NULL,
    tutor          VARCHAR(100) NOT NULL,
    pet            VARCHAR(100) NOT NULL,
    servico        VARCHAR(100) NOT NULL,
    data           VARCHAR(10)  NOT NULL, -- DD/MM/AAAA
    hora           VARCHAR(5)   NOT NULL, -- HH:MM
    status         VARCHAR(20)  NOT NULL
);

-- ==========================
-- TABELA: vendas
-- ==========================
CREATE TABLE IF NOT EXISTS vendas (
    codigo INT           NOT NULL PRIMARY KEY,
    itens  LONGTEXT      NOT NULL,       -- JSON com itens da venda
    total  DECIMAL(10,2) NOT NULL,
    data   VARCHAR(10)   NOT NULL        -- DD/MM/AAAA
);
