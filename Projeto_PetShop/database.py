import json
import mysql.connector

# Importa as configurações e utilitários
import config
import utils

# ======================================================================
# DADOS GLOBAIS EM MEMÓRIA
# ======================================================================
# Estas listas são importadas por outros módulos (CRUD)
# e são preenchidas pela função carregar_dados()

produtos = []
clientes = []
usuarios = {}  # Dicionário
agendamentos = []
vendas = []
servicos = []

proximo_codigo_produto = 1
proximo_codigo_cliente = 1
proximo_codigo_agendamento = 1
proximo_codigo_venda = 1
proximo_codigo_servico = 1

# ======================================================================
# FUNÇÕES DE CONEXÃO
# ======================================================================

def get_server_conn():
    """Conexão sem selecionar database (para criar o banco)."""
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
    )


def get_conn():
    """Conexão já apontando para o banco de dados."""
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
    )

# ======================================================================
# INICIALIZAÇÃO / CARGA / SALVAMENTO
# ======================================================================

def inicializar_banco():
    """Cria banco e tabelas, se ainda não existirem."""
    print("Inicializando banco de dados...")
    # Cria o banco, se não existir
    try:
        conn = get_server_conn()
        cur = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB} "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cur.close()
        conn.close()

        # Cria as tabelas
        conn = get_conn()
        cur = conn.cursor()

        # Produtos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                codigo    INT           NOT NULL PRIMARY KEY,
                nome      VARCHAR(100)  NOT NULL,
                quantidade INT          NOT NULL,
                preco     DECIMAL(10,2) NOT NULL,
                validade  VARCHAR(10)
            )
        """)

        # Serviços
        cur.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                codigo    INT           NOT NULL PRIMARY KEY,
                nome      VARCHAR(100)  NOT NULL,
                descricao TEXT,
                preco     DECIMAL(10,2) NOT NULL
            )
        """)

        # Clientes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                codigo   INT          NOT NULL PRIMARY KEY,
                tutor    VARCHAR(100) NOT NULL,
                pet      VARCHAR(100) NOT NULL,
                raca     VARCHAR(100) NOT NULL,
                servico  VARCHAR(100)
            )
        """)

        # Usuários
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario VARCHAR(50)  NOT NULL PRIMARY KEY,
                senha   VARCHAR(64)  NOT NULL,
                perfil  VARCHAR(10)  NOT NULL,
                email   VARCHAR(255) NOT NULL UNIQUE
            )
        """)

        # Agendamentos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                codigo         INT          NOT NULL PRIMARY KEY,
                cliente_codigo INT          NOT NULL,
                tutor          VARCHAR(100) NOT NULL,
                pet            VARCHAR(100) NOT NULL,
                servico        VARCHAR(100) NOT NULL,
                data           VARCHAR(10)  NOT NULL,  -- DD/MM/AAAA
                hora           VARCHAR(5)   NOT NULL,  -- HH:MM
                `status`       VARCHAR(20)  NOT NULL
            )
        """)

        # Vendas (itens em JSON)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                codigo INT           NOT NULL PRIMARY KEY,
                itens  LONGTEXT      NOT NULL,  -- JSON
                total  DECIMAL(10,2) NOT NULL,
                data   VARCHAR(10)   NOT NULL   -- DD/MM/AAAA
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Banco de dados e tabelas verificados com sucesso.")
    except mysql.connector.Error as err:
        print(f"❌ Erro ao inicializar o banco: {err}")
        print("Verifique se o MySQL está rodando e se as credenciais em 'config.py' estão corretas.")
        exit() # Sai do programa se não puder conectar


def carregar_dados():
    """Carrega todos os dados do MySQL para as listas em memória."""
    global produtos, clientes, usuarios, agendamentos, vendas, servicos
    global proximo_codigo_produto, proximo_codigo_cliente
    global proximo_codigo_agendamento, proximo_codigo_venda, proximo_codigo_servico
    
    print("Carregando dados do banco...")
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        # Produtos
        cur.execute("SELECT * FROM produtos")
        produtos = cur.fetchall()
        proximo_codigo_produto = max([p["codigo"] for p in produtos], default=0) + 1

        # Clientes
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        proximo_codigo_cliente = max([c["codigo"] for c in clientes], default=0) + 1

        # Usuários
        cur.execute("SELECT * FROM usuarios")
        usuarios.clear()
        for row in cur.fetchall():
            usuarios[row["usuario"]] = {
                "senha": row["senha"],
                "perfil": row["perfil"],
                "email": row["email"],
            }

        # Se não tiver nenhum usuário, cria admin e user padrão
        if not usuarios:
            print("Nenhum usuário encontrado. Criando usuários padrão 'admin' e 'user'...")
            usuarios.update(
                {
                    "admin": {
                        "senha": utils.gerar_hash("admin123"),
                        "perfil": "admin",
                        "email": "admin@email.com",
                    },
                    "user": {
                        "senha": utils.gerar_hash("user123"),
                        "perfil": "user",
                        "email": "user@email.com",
                    },
                }
            )
            # Salva os novos usuários padrão imediatamente
            salvar_dados(primeira_carga=True)

        # Agendamentos
        cur.execute("SELECT * FROM agendamentos")
        agendamentos = cur.fetchall()
        proximo_codigo_agendamento = (
            max([a["codigo"] for a in agendamentos], default=0) + 1
        )

        # Vendas
        cur.execute("SELECT * FROM vendas")
        vendas = []
        for row in cur.fetchall():
            venda = dict(row)
            if isinstance(venda.get("itens"), str):
                try:
                    venda["itens"] = json.loads(venda["itens"])
                except Exception:
                    venda["itens"] = []
            else:
                venda["itens"] = []
            vendas.append(venda)
        proximo_codigo_venda = max([v["codigo"] for v in vendas], default=0) + 1

        # Serviços
        cur.execute("SELECT * FROM servicos")
        servicos = cur.fetchall()
        proximo_codigo_servico = (
            max([s["codigo"] for s in servicos], default=0) + 1
        )

        conn.close()
        print("Dados carregados com sucesso.")
    except Exception as e:
        print(f"❌ Erro fatal ao carregar dados: {e}")
        exit()


def salvar_dados(primeira_carga=False):
    """Salva o estado atual das listas em memória de volta no MySQL."""
    
    # Evita salvar se estivermos na primeira carga (para não truncar os usuários recém-criados)
    if not primeira_carga and not usuarios:
         # Se 'usuarios' está vazio e não é a primeira carga, algo está muito errado.
         print("❌ Erro crítico: Tentativa de salvar dados sem usuários carregados. Abortando.")
         return

    try:
        conn = get_conn()
        cur = conn.cursor()

        # Produtos
        cur.execute("TRUNCATE TABLE produtos")
        if produtos:
            for p in produtos:
                cur.execute(
                    """
                    INSERT INTO produtos (codigo, nome, quantidade, preco, validade)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (p["codigo"], p["nome"], p["quantidade"], p["preco"], p["validade"]),
                )

        # Clientes
        cur.execute("TRUNCATE TABLE clientes")
        if clientes:
            for c in clientes:
                cur.execute(
                    """
                    INSERT INTO clientes (codigo, tutor, pet, raca, servico)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (c["codigo"], c["tutor"], c["pet"], c["raca"], c["servico"]),
                )

        # Usuários
        cur.execute("TRUNCATE TABLE usuarios")
        if usuarios:
            for u, v in usuarios.items():
                cur.execute(
                    """
                    INSERT INTO usuarios (usuario, senha, perfil, email)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (u, v["senha"], v["perfil"], v["email"]),
                )

        # Agendamentos
        cur.execute("TRUNCATE TABLE agendamentos")
        if agendamentos:
            for a in agendamentos:
                cur.execute(
                    """
                    INSERT INTO agendamentos
                        (codigo, cliente_codigo, tutor, pet, servico, data, hora, `status`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        a["codigo"], a["cliente_codigo"], a["tutor"], a["pet"],
                        a["servico"], a["data"], a["hora"], a["status"],
                    ),
                )

        # Vendas
        cur.execute("TRUNCATE TABLE vendas")
        if vendas:
            for v in vendas:
                cur.execute(
                    """
                    INSERT INTO vendas (codigo, itens, total, data)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        v["codigo"], json.dumps(v["itens"]), v["total"], v["data"],
                    ),
                )

        # Serviços
        cur.execute("TRUNCATE TABLE servicos")
        if servicos:
            for s in servicos:
                cur.execute(
                    """
                    INSERT INTO servicos (codigo, nome, descricao, preco)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (s["codigo"], s["nome"], s["descricao"], s["preco"]),
                )

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")