import pandas as pd
import database
import crud_servicos  # Importa para poder usar o listar_servicos()

# ======================================================================
# FUNÇÕES DE CLIENTES
# ======================================================================

def adicionar_cliente():
    global proximo_codigo_cliente
    print("\n--- Adicionar Novo Cliente ---")

    # REMOVIDO: Bloco 'if not servicos:' que impedia o cadastro
    # Agora é possível cadastrar um cliente mesmo sem serviços no sistema.

    tutor = input("Nome do tutor: ")
    pet = input("Nome do animal: ")
    raca = input("Raça do animal: ")

    servico = None  # <-- MUDANÇA: Serviço começa como nulo (None) por padrão

    # A seleção de serviço agora é opcional e só aparece se houver serviços
    if database.servicos:
        print("\nServiços disponíveis (Opcional):")
        crud_servicos.listar_servicos() # Usa a função do outro módulo
        while True:
            try:
                # MUDANÇA: Texto do input alterado para incluir "Enter para pular"
                codigo_servico = input(
                    "\nDigite o código do serviço (ou Enter para pular, '0' para cancelar): "
                )

                if codigo_servico == "0":
                    print("❌ Cadastro de cliente cancelado.")
                    return

                # MUDANÇA: Verifica se o usuário apenas pressionou Enter
                if not codigo_servico:
                    servico = None
                    print("ℹ️ Nenhum serviço selecionado para este cliente.")
                    break  # Sai do loop

                # Só tenta converter para int se não for vazio
                codigo_servico_int = int(codigo_servico)
                servico_encontrado = next(
                    (s for s in database.servicos if s["codigo"] == codigo_servico_int), None
                )

                if servico_encontrado:
                    servico = servico_encontrado["nome"]
                    break
                else:
                    print("❌ Código de serviço inválido. Tente novamente.")
            except ValueError:
                print("\n❌ Erro: O código do serviço deve ser um número inteiro.")
    else:
        print("\nℹ️ Nenhum serviço cadastrado no sistema. Cliente será salvo sem serviço.")

    cliente = {
        "codigo": database.proximo_codigo_cliente,
        "tutor": tutor,
        "pet": pet,
        "raca": raca,
        "servico": servico,  # <-- MUDANÇA: Salva o valor (pode ser None)
    }
    database.clientes.append(cliente)
    database.proximo_codigo_cliente += 1
    database.salvar_dados()

    # MUDANÇA: Mensagem de sucesso condicional
    if servico:
        print(
            f"\n✅ Cliente '{tutor}' (pet: {pet}) adicionado com sucesso com serviço '{servico}'!"
        )
    else:
        print(
            f"\n✅ Cliente '{tutor}' (pet: {pet}) adicionado com sucesso (sem serviço)!"
        )


def listar_clientes():
    print("\n--- Lista de Clientes ---")
    if not database.clientes:
        print("Nenhum cliente cadastrado.")
        return
    df = pd.DataFrame(database.clientes, columns=["codigo", "tutor", "pet", "raca", "servico"])
    
    # Preenche valores nulos (None) com um traço '—' para exibição
    df_display = df.fillna('—')
    
    print(
        df_display.to_string(
            index=False,
            col_space={"codigo": 10, "tutor": 30, "pet": 30, "raca": 30, "servico": 30},
        )
    )
    print("-" * 150)


def editar_cliente():
    print("\n--- Editar Cliente ---")
    listar_clientes()
    if not database.clientes:
        return
    try:
        codigo = int(input("\nDigite o código do cliente para editar: "))
        cliente_encontrado = next((c for c in database.clientes if c["codigo"] == codigo), None)
        if cliente_encontrado:
            print(
                f"Editando cliente: {cliente_encontrado['tutor']} (pet: {cliente_encontrado['pet']})"
            )
            novo_tutor = input(f"Novo nome do tutor ({cliente_encontrado['tutor']}): ")
            tutor = novo_tutor if novo_tutor else cliente_encontrado["tutor"]

            novo_pet = input(f"Novo nome do pet ({cliente_encontrado['pet']}): ")
            pet = novo_pet if novo_pet else cliente_encontrado["pet"]

            nova_raca = input(f"Nova raça do animal ({cliente_encontrado['raca']}): ")
            raca = nova_raca if nova_raca else cliente_encontrado["raca"]

            print("\nServiços disponíveis:")
            crud_servicos.listar_servicos()
            while True:
                try:
                    # MUDANÇA: Adicionada a opção 'N' para remover o serviço
                    servico_atual = cliente_encontrado['servico'] if cliente_encontrado['servico'] else "Nenhum"
                    codigo_servico = input(
                        f"\nDigite o código do novo serviço (Enter para manter '{servico_atual}', 'N' para remover): "
                    )
                    
                    # MUDANÇA: Opção de Manter (Enter)
                    if not codigo_servico:
                        servico = cliente_encontrado["servico"]
                        break
                    
                    # MUDANÇA: Opção de Remover ('N')
                    if codigo_servico.upper() == 'N':
                        servico = None
                        print("ℹ️ Serviço removido do cliente.")
                        break

                    # Tenta converter para int (escolher novo serviço)
                    codigo_servico_int = int(codigo_servico)
                    novo_servico_obj = next(
                        (s for s in database.servicos if s["codigo"] == codigo_servico_int), None
                    )
                    
                    if novo_servico_obj:
                        servico = novo_servico_obj["nome"]
                        break
                    else:
                        print("❌ Código de serviço inválido. Tente novamente.")
                except ValueError:
                    print("\n❌ Erro: O código do serviço deve ser um número inteiro.")
            
            cliente_encontrado.update(
                {"tutor": tutor, "pet": pet, "raca": raca, "servico": servico}
            )
            database.salvar_dados()
            print("\n✅ Cliente atualizado com sucesso!")
        else:
            print("❌ Cliente não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")


def remover_cliente():
    print("\n--- Remover Cliente ---")
    listar_clientes()
    if not database.clientes:
        return
    try:
        codigo = int(input("\nDigite o código do cliente para remover: "))
        cliente_encontrado = next((c for c in database.clientes if c["codigo"] == codigo), None)
        if cliente_encontrado:
            agendamentos_cliente = [
                a for a in database.agendamentos if a["cliente_codigo"] == codigo
            ]
            if agendamentos_cliente:
                print(
                    "\n❌ Erro: Não é possível remover o cliente, pois ele possui agendamentos associados."
                )
                return
            database.clientes.remove(cliente_encontrado)
            database.salvar_dados()
            print(
                f"\n✅ Cliente '{cliente_encontrado['tutor']}' (pet: {cliente_encontrado['pet']}) removido com sucesso!"
            )
        else:
            print("❌ Cliente não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")