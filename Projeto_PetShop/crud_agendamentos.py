import pandas as pd
import database
import utils
import notifications
import crud_clientes  # Para listar clientes
import crud_servicos  # Para listar serviços

# ======================================================================
# FUNÇÕES DE AGENDAMENTOS
# ======================================================================

def adicionar_agendamento():
    print("\n--- Adicionar Novo Agendamento ---")
    crud_clientes.listar_clientes()
    if not database.clientes:
        print("❌ Não é possível adicionar agendamento: nenhum cliente cadastrado.")
        return
    try:
        codigo_cliente = int(input("Digite o código do cliente: "))
        cliente_encontrado = next(
            (c for c in database.clientes if c["codigo"] == codigo_cliente), None
        )
        if not cliente_encontrado:
            print("❌ Cliente não encontrado.")
            return
            
        data = input("Data do agendamento (DD/MM/AAAA): ")
        if not utils.validar_data(data):
            print("\n❌ Erro: Data inválida. Use o formato DD/MM/AAAA.")
            return
            
        hora = input("Hora do agendamento (HH:MM): ")
        if not utils.validar_hora(hora):
            print("\n❌ Erro: Hora inválida. Use o formato HH:MM.")
            return
            
        print("\nServiços disponíveis:")
        crud_servicos.listar_servicos()
        if not database.servicos:
             print("❌ Nenhum serviço cadastrado. Cancele e cadastre um serviço primeiro.")
             return

        while True:
            try:
                codigo_servico = input(
                    "\nDigite o código do serviço (ou '0' para cancelar): "
                )
                if codigo_servico == "0":
                    print("❌ Cadastro de agendamento cancelado.")
                    return
                
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
                
        agendamento = {
            "codigo": database.proximo_codigo_agendamento,
            "cliente_codigo": codigo_cliente,
            "tutor": cliente_encontrado["tutor"],
            "pet": cliente_encontrado["pet"],
            "servico": servico,
            "data": data,
            "hora": hora,
            "status": "Pendente",
        }
        database.agendamentos.append(agendamento)
        database.proximo_codigo_agendamento += 1
        database.salvar_dados()
        
        notifications.enviar_notificacao_agendamento(
            cliente_encontrado["tutor"],
            cliente_encontrado["pet"],
            servico,
            data,
            hora,
        )
        print(
            f"\n✅ Agendamento para '{cliente_encontrado['tutor']}' (pet: {cliente_encontrado['pet']}) adicionado com sucesso!"
        )
    except ValueError:
        print("\n❌ Erro: O código do cliente deve ser um número inteiro.")


def listar_agendamentos():
    print("\n--- Lista de Agendamentos ---")
    if not database.agendamentos:
        print("Nenhum agendamento cadastrado.")
        return
    df = pd.DataFrame(
        database.agendamentos,
        columns=[
            "codigo", "cliente_codigo", "tutor", "pet",
            "servico", "data", "hora", "status",
        ],
    )
    print(
        df.to_string(
            index=False,
            col_space={
                "codigo": 10, "cliente_codigo": 15, "tutor": 30, "pet": 30,
                "servico": 30, "data": 15, "hora": 10, "status": 12,
            },
        )
    )
    print("-" * 150)


def editar_agendamento():
    print("\n--- Editar Agendamento ---")
    listar_agendamentos()
    if not database.agendamentos:
        return
    try:
        codigo = int(input("\nDigite o código do agendamento para editar: "))
        agendamento_encontrado = next(
            (a for a in database.agendamentos if a["codigo"] == codigo), None
        )
        if agendamento_encontrado:
            print(
                f"Editando agendamento para: {agendamento_encontrado['tutor']} (pet: {agendamento_encontrado['pet']})"
            )
            data = (
                input(f"Nova data ({agendamento_encontrado['data']}): ")
                or agendamento_encontrado["data"]
            )
            if data and not utils.validar_data(data):
                print("\n❌ Erro: Data inválida. Use o formato DD/MM/AAAA.")
                return
                
            hora = (
                input(f"Nova hora ({agendamento_encontrado['hora']}): ")
                or agendamento_encontrado["hora"]
            )
            if hora and not utils.validar_hora(hora):
                print("\n❌ Erro: Hora inválida. Use o formato HH:MM.")
                return
                
            print("\nServiços disponíveis:")
            crud_servicos.listar_servicos()
            while True:
                try:
                    codigo_servico = input(
                        f"\nDigite o código do novo serviço (ou Enter para manter '{agendamento_encontrado['servico']}'): "
                    )
                    if not codigo_servico:
                        servico = agendamento_encontrado["servico"]
                        break
                        
                    codigo_servico_int = int(codigo_servico)
                    servico_encontrado_obj = next(
                        (s for s in database.servicos if s["codigo"] == codigo_servico_int), None
                    )
                    if servico_encontrado_obj:
                        servico = servico_encontrado_obj["nome"]
                        break
                    else:
                        print("❌ Código de serviço inválido. Tente novamente.")
                except ValueError:
                    print("\n❌ Erro: O código do serviço deve ser um número inteiro.")
                    
            status = (
                input(f"Novo status ({agendamento_encontrado['status']}): ")
                or agendamento_encontrado["status"]
            )
            
            agendamento_encontrado.update(
                {"data": data, "hora": hora, "servico": servico, "status": status}
            )
            database.salvar_dados()
            print("\n✅ Agendamento atualizado com sucesso!")
        else:
            print("❌ Agendamento não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")


def remover_agendamento():
    print("\n--- Cancelar Agendamento ---")
    listar_agendamentos()
    if not database.agendamentos:
        return
    try:
        codigo = int(input("\nDigite o código do agendamento para cancelar: "))
        agendamento_encontrado = next(
            (a for a in database.agendamentos if a["codigo"] == codigo), None
        )
        if agendamento_encontrado:
            notifications.enviar_notificacao_cancelamento_agendamento(
                agendamento_encontrado["tutor"],
                agendamento_encontrado["pet"],
                agendamento_encontrado["servico"],
                agendamento_encontrado["data"],
                agendamento_encontrado["hora"],
            )
            database.agendamentos.remove(agendamento_encontrado)
            database.salvar_dados()
            print(
                f"\n✅ Agendamento para '{agendamento_encontrado['tutor']}' removido com sucesso!"
            )
        else:
            print("❌ Agendamento não encontrado.")
    except ValueError:
        print("\n❌ Erro: O código deve ser um número inteiro.")