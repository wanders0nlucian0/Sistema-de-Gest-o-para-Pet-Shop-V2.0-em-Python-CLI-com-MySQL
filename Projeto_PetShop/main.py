#Versão 2.0
from getpass import getpass

# Importa os módulos principais do sistema
import database
import utils
import auth
import menus
import crud_usuarios # Necessário para a função de recuperar senha

# ======================================================================
# FUNÇÕES DE LOGIN PRINCIPAL
# ======================================================================

def fazer_login():
    print("\n--- TELA DE LOGIN ---")
    usuario_input = input("Usuário: ")
    senha_input = getpass("Senha: ")
    
    # Verifica se o usuário existe e se a senha (hasheada) bate
    if usuario_input in database.usuarios and \
       database.usuarios[usuario_input]["senha"] == utils.gerar_hash(senha_input):
        
        print(f"\nLogin bem-sucedido! Bem-vindo(a), {usuario_input}.")
        auth.usuario_logado = usuario_input # Define o usuário logado na sessão
        return database.usuarios[usuario_input]["perfil"] # Retorna 'admin' ou 'user'
    else:
        print("\n❌ Usuário ou senha incorretos.")
        return None

# ======================================================================
# PROGRAMA PRINCIPAL
# ======================================================================

def main():
    """Função principal que executa o programa."""
    try:
        database.inicializar_banco()
        database.carregar_dados()
    except Exception as e:
        print(f"❌ Erro crítico ao iniciar o sistema: {e}")
        print("O programa será encerrado.")
        return # Encerra a função main

    while True:
        utils.limpar_tela()
        print("=" * 60)
        print("       Bem-vindo ao Sistema de Gestão Meu Querido Pet       ")
        print("=" * 60)
        print("\n1 - Fazer Login")
        print("2 - Recuperar Senha")
        print("0 - Sair do Programa")
        
        escolha_inicial = input("Escolha uma opção: ")
        
        if escolha_inicial == "1":
            perfil_logado = fazer_login()
            if perfil_logado == "admin":
                menus.menu_admin()
            elif perfil_logado == "user":
                menus.menu_usuario()
            else:
                input("\nPressione Enter para voltar ao menu principal...")
                
        elif escolha_inicial == "2":
            crud_usuarios.recuperar_senha_db() # Chama a função de recuperação
            input("\nPressione Enter para voltar ao menu principal...")
            
        elif escolha_inicial == "0":
            break
            
        else:
            print("❌ Opção inválida.")
            input("\nPressione Enter para continuar...")

    print("\nPrograma encerrado.")


# Este é o ponto de entrada do seu programa
if __name__ == "__main__":
    main()