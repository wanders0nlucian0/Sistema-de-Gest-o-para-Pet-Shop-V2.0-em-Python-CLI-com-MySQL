import pandas as pd
import database

# ======================================================================
# FUNÇÕES DE SERVIÇOS
# ======================================================================

def adicionar_servico():
    print("\n--- Adicionar Novo Serviço ---")
    nome = input("Nome do serviço: ")
    descricao = input("Descrição do serviço: ")
    try:
        preco = float(input("Preço do serviço (ex: 50.00): "))
        servico = {
            "codigo": database.proximo_codigo_servico,
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
        }
        database.servicos.append(servico)
        database.proximo_codigo_servico += 1
        database.salvar_dados()
        print(f"\n✅ Serviço '{nome}' adicionado com sucesso!")
    except ValueError:
        print("\n❌ Erro: O preço deve ser um número.")


def listar_servicos():
    print("\n--- Lista de Serviços ---")
    if not database.servicos:
        print("Nenhum serviço cadastrado.")
        return
    df = pd.DataFrame(database.servicos, columns=["codigo", "nome", "descricao", "preco"])
    print(
        df.to_string(
            index=False,
            col_space={"codigo": 10, "nome": 30, "descricao": 50, "preco": 12},
        )
    )
    print("-" * 110)


def editar_servico():
    print("\n--- Editar Serviço ---")
    listar_servicos()
    if not database.servicos:
        return
    try:
        codigo = int(input("\nDigite o código do serviço para editar: "))
        servico_encontrado = next((s for s in database.servicos if s["codigo"] == codigo), None)
        
        if servico_encontrado:
            print(f"Editando serviço: {servico_encontrado['nome']}")
            servico_encontrado["nome"] = (
                input(f"Novo nome ({servico_encontrado['nome']}): ")
                or servico_encontrado["nome"]
            )
            servico_encontrado["descricao"] = (
                input(f"Nova descrição ({servico_encontrado['descricao']}): ")
                or servico_encontrado["descricao"]
            )
            preco = input(f"Novo preço ({servico_encontrado['preco']}): ")
            servico_encontrado["preco"] = (
                float(preco) if preco else servico_encontrado["preco"]
            )
            database.salvar_dados()
            print("\n✅ Serviço atualizado com sucesso!")
        else:
            print("❌ Serviço não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código e preço devem ser números.")


def remover_servico():
    print("\n--- Remover Serviço ---")
    listar_servicos()
    if not database.servicos:
        return
    try:
        codigo = int(input("\nDigite o código do serviço para remover: "))
        servico_encontrado = next((s for s in database.servicos if s["codigo"] == codigo), None)
        
        if servico_encontrado:
            # Verifica dependências em clientes e agendamentos
            clientes_com_servico = [
                c for c in database.clientes if c["servico"] == servico_encontrado["nome"]
            ]
            agendamentos_com_servico = [
                a for a in database.agendamentos if a["servico"] == servico_encontrado["nome"]
            ]
            
            if clientes_com_servico or agendamentos_com_servico:
                print(
                    "\n❌ Erro: Não é possível remover o serviço, pois ele está associado a clientes ou agendamentos."
                )
                return
                
            database.servicos.remove(servico_encontrado)
            database.salvar_dados()
            print(f"\n✅ Serviço '{servico_encontrado['nome']}' removido com sucesso!")
        else:
            print("❌ Serviço não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")