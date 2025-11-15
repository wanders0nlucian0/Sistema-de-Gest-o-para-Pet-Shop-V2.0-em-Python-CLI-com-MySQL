import pandas as pd
import database  # Importa o módulo database
import utils     # Importa o módulo utils
import notifications # Importa as notificações

# ======================================================================
# FUNÇÕES DE PRODUTOS
# ======================================================================

def adicionar_produto():
    print("\n--- Adicionar Novo Produto ---")
    try:
        nome = input("Nome do produto: ")
        quantidade = int(input("Quantidade em estoque: "))
        preco = float(input("Preço unitário (ex: 25.50): "))
        validade = input("Data de validade (DD/MM/AAAA): ")
        if not utils.validar_data(validade):
            print("\n❌ Erro: Data de validade inválida. Use o formato DD/MM/AAAA.")
            return
        
        produto = {
            "codigo": database.proximo_codigo_produto,
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco,
            "validade": validade,
        }
        
        # Acessa a lista de produtos e o contador do módulo database
        database.produtos.append(produto)
        database.proximo_codigo_produto += 1
        
        database.salvar_dados() # Salva no banco
        notifications.enviar_notificacao_estoque(nome, quantidade)
        print(f"\n✅ Produto '{nome}' adicionado com sucesso!")
        
    except ValueError:
        print("\n❌ Erro: Quantidade e preço devem ser números.")


def listar_produtos():
    print("\n--- Lista de Produtos em Estoque ---")
    if not database.produtos:
        print("Nenhum produto cadastrado.")
        return
    df = pd.DataFrame(
        database.produtos, columns=["codigo", "nome", "quantidade", "preco", "validade"]
    )
    print(
        df.to_string(
            index=False,
            col_space={
                "codigo": 10, "nome": 30, "quantidade": 15,
                "preco": 12, "validade": 15,
            },
        )
    )
    print("-" * 90)


def editar_produto():
    print("\n--- Editar Produto ---")
    listar_produtos()
    if not database.produtos:
        return
    try:
        codigo = int(input("\nDigite o código do produto para editar: "))
        produto_encontrado = next((p for p in database.produtos if p["codigo"] == codigo), None)
        
        if produto_encontrado:
            print(f"Editando produto: {produto_encontrado['nome']}")
            produto_encontrado["nome"] = (
                input(f"Novo nome ({produto_encontrado['nome']}): ")
                or produto_encontrado["nome"]
            )
            quantidade = input(
                f"Nova quantidade ({produto_encontrado['quantidade']}): "
            )
            produto_encontrado["quantidade"] = (
                int(quantidade) if quantidade else produto_encontrado["quantidade"]
            )
            preco = input(f"Novo preço ({produto_encontrado['preco']}): ")
            produto_encontrado["preco"] = (
                float(preco) if preco else produto_encontrado["preco"]
            )
            validade = (
                input(f"Nova validade ({produto_encontrado['validade']}): ")
                or produto_encontrado["validade"]
            )
            if validade and not utils.validar_data(validade):
                print("\n❌ Erro: Data de validade inválida. Use o formato DD/MM/AAAA.")
                return
            
            produto_encontrado["validade"] = validade
            database.salvar_dados()
            
            notifications.enviar_notificacao_estoque(
                produto_encontrado["nome"], produto_encontrado["quantidade"]
            )
            print("\n✅ Produto atualizado com sucesso!")
        else:
            print("❌ Produto não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código, quantidade e preço devem ser números.")


def remover_produto():
    print("\n--- Remover Produto ---")
    listar_produtos()
    if not database.produtos:
        return
    try:
        codigo = int(input("\nDigite o código do produto para remover: "))
        produto_encontrado = next((p for p in database.produtos if p["codigo"] == codigo), None)
        
        if produto_encontrado:
            database.produtos.remove(produto_encontrado)
            database.salvar_dados()
            print(f"\n✅ Produto '{produto_encontrado['nome']}' removido com sucesso!")
        else:
            print("❌ Produto não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")


def relatorio_estoque():
    print("\n--- Relatório de Estoque ---")
    if not database.produtos:
        print("Nenhum produto cadastrado.")
        return
    
    df = pd.DataFrame(
        database.produtos, columns=["codigo", "nome", "quantidade", "preco", "validade"]
    )
    df["valor_total"] = df["quantidade"] * df["preco"]
    df["status"] = df["quantidade"].apply(
        lambda q: "Baixo" if q <= 5 else "Alto" if q >= 30 else "Normal"
    )
    
    print(
        df.to_string(
            index=False,
            col_space={
                "codigo": 10, "nome": 30, "quantidade": 15, "preco": 12,
                "validade": 15, "valor_total": 15, "status": 10,
            },
        )
    )
    print("-" * 110)
    total_itens = df["quantidade"].sum()
    total_valor = df["valor_total"].sum()
    print(f"\nTotal de itens em estoque: {total_itens}")
    print(f"Valor total estimado do estoque: R${total_valor:.2f}")