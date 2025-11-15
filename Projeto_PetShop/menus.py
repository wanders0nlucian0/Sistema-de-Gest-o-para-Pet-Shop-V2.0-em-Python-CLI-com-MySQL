import utils
import auth

# Importa todos os módulos de CRUD (gerenciamento)
import crud_produtos
import crud_servicos
import crud_clientes
import crud_agendamentos
import crud_vendas
import crud_usuarios

# ======================================================================
# MENUS DE NAVEGAÇÃO
# ======================================================================

def menu_admin():
    while True:
        utils.limpar_tela()
        print("\n===== MENU DO ADMINISTRADOR =====")
        print("--- PRODUTOS ---")
        print("1. Adicionar Produto   | 2. Listar Produtos")
        print("3. Editar Produto      | 4. Remover Produto")
        print("5. Relatório de Estoque")
        print("--- CLIENTES ---")
        print("6. Adicionar Cliente   | 7. Listar Clientes")
        print("8. Editar Cliente      | 9. Remover Cliente")
        print("--- AGENDAMENTOS ---")
        print("10. Adicionar Agendamento | 11. Listar Agendamentos")
        print("12. Editar Agendamento    | 13. Cancelar Agendamento")
        print("--- VENDAS ---")
        print("14. Registrar Venda       | 15. Listar Vendas")
        print("16. Cancelar Venda        | 17. Totais de Vendas")
        print("27. Relatório de Vendas (estatísticas e gráfico)")
        print("--- USUÁRIOS ---")
        print("18. Adicionar Usuário   | 19. Listar Usuários")
        print("20. Editar Usuário      | 21. Remover Usuário")
        print("22. Alterar Minha Senha")
        print("--- SERVIÇOS ---")
        print("23. Adicionar Serviço   | 24. Listar Serviços")
        print("25. Editar Serviço      | 26. Remover Serviço")
        print("--------------------")
        print("0. Fazer Logout")
        
        opcao = input("Escolha uma opção: ")
        
        # Mapeamento de opções para funções
        opcoes = {
            "1": crud_produtos.adicionar_produto,
            "2": crud_produtos.listar_produtos,
            "3": crud_produtos.editar_produto,
            "4": crud_produtos.remover_produto,
            "5": crud_produtos.relatorio_estoque,
            "6": crud_clientes.adicionar_cliente,
            "7": crud_clientes.listar_clientes,
            "8": crud_clientes.editar_cliente,
            "9": crud_clientes.remover_cliente,
            "10": crud_agendamentos.adicionar_agendamento,
            "11": crud_agendamentos.listar_agendamentos,
            "12": crud_agendamentos.editar_agendamento,
            "13": crud_agendamentos.remover_agendamento,
            "14": crud_vendas.registrar_venda,
            "15": crud_vendas.listar_vendas,
            "16": crud_vendas.remover_venda,
            "17": crud_vendas.calcular_totais_vendas,
            "18": crud_usuarios.adicionar_usuario,
            "19": crud_usuarios.listar_usuarios,
            "20": crud_usuarios.editar_usuario,
            "21": crud_usuarios.remover_usuario,
            "22": crud_usuarios.editar_senha_usuario,
            "23": crud_servicos.adicionar_servico,
            "24": crud_servicos.listar_servicos,
            "25": crud_servicos.editar_servico,
            "26": crud_servicos.remover_servico,
            "27": crud_vendas.relatorio_vendas,
        }
        
        if opcao == "0":
            print("\nFazendo logout...")
            auth.usuario_logado = None
            break
        
        # Pega a função correspondente no dicionário
        funcao_a_executar = opcoes.get(opcao)
        
        if funcao_a_executar:
            funcao_a_executar() # Executa a função
        else:
            print("\n❌ Opção inválida.")
            
        input("\nPressione Enter para continuar...")


def menu_usuario():
    while True:
        utils.limpar_tela()
        print("\n===== MENU DO USUÁRIO =====")
        print("1. Listar Produtos")
        print("2. Listar Clientes")
        print("3. Adicionar Cliente")
        print("4. Adicionar Agendamento")
        print("5. Listar Agendamentos")
        print("6. Registrar Venda")
        print("7. Listar Vendas")
        print("8. Alterar Minha Senha")
        print("9. Listar Serviços")
        print("10. Relatório de Vendas (estatísticas e gráfico)")
        print("--------------------")
        print("0. Fazer Logout")
        
        opcao = input("Escolha uma opção: ")
        
        # Mapeamento de opções para funções
        opcoes = {
            "1": crud_produtos.listar_produtos,
            "2": crud_clientes.listar_clientes,
            "3": crud_clientes.adicionar_cliente,
            "4": crud_agendamentos.adicionar_agendamento,
            "5": crud_agendamentos.listar_agendamentos,
            "6": crud_vendas.registrar_venda,
            "7": crud_vendas.listar_vendas,
            "8": crud_usuarios.editar_senha_usuario,
            "9": crud_servicos.listar_servicos,
            "10": crud_vendas.relatorio_vendas,
        }

        if opcao == "0":
            print("\nFazendo logout...")
            auth.usuario_logado = None
            break
        
        funcao_a_executar = opcoes.get(opcao)
        
        if funcao_a_executar:
            funcao_a_executar() # Executa a função
        else:
            print("\n❌ Opção inválida.")
            
        input("\nPressione Enter para continuar...")