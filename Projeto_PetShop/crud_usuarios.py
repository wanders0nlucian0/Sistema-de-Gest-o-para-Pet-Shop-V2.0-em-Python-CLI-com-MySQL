import pandas as pd
from getpass import getpass
import string
import random

import database
import utils
import notifications
import auth

# ======================================================================
# FUNÇÕES DE USUÁRIOS
# ======================================================================

def adicionar_usuario():
    print("\n--- Adicionar Novo Usuário ---")
    nome = input("Nome de usuário: ")
    if nome in database.usuarios:
        print("❌ Usuário já existe.")
        return
    email_usuario = input("E-mail do usuário: ")
    senha = getpass("Senha: ")
    if not senha:
        print("❌ A senha não pode ser vazia.")
        return
    perfil = input("Perfil (admin/user): ").lower()
    if perfil not in ["admin", "user"]:
        print("❌ Perfil inválido. Use 'admin' ou 'user'.")
        return
        
    database.usuarios[nome] = {
        "senha": utils.gerar_hash(senha),
        "perfil": perfil,
        "email": email_usuario,
    }
    database.salvar_dados()

    corpo_email = f"""
    <h3>Bem-vindo ao Sistema Meu Querido Pet!</h3>
    <p>Olá, {nome}!</p>
    <p>Sua conta foi criada com sucesso no sistema Meu Querido Pet.</p>
    <p><b>Detalhes da Conta:</b></p>
    <p>Usuário: {nome}</p>
    <p>Perfil: {perfil}</p>
    <p>Senha inicial: {senha}</p>
    <p>Recomendamos que você altere sua senha após o primeiro login.</p>
    <p>Atenciosamente,</p>
    <p>Equipe Meu Querido Pet</p>
    """
    notifications.enviar_email(email_usuario, "Bem-vindo ao Meu Querido Pet", corpo_email)

    print(f"\n✅ Usuário '{nome}' adicionado com sucesso!")


def listar_usuarios():
    print("\n--- Lista de Usuários ---")
    if not database.usuarios:
        print("Nenhum usuário cadastrado.")
        return
    df = pd.DataFrame(
        [
            {"Usuário": u, "Perfil": v["perfil"], "E-mail": v["email"]}
            for u, v in database.usuarios.items()
        ]
    )
    print(
        df.to_string(index=False, col_space={"Usuário": 30, "Perfil": 12, "E-mail": 40})
    )
    print("-" * 90)


def editar_usuario():
    print("\n--- Editar Usuário ---")
    listar_usuarios()
    if not database.usuarios:
        return
    nome_usuario = input("\nDigite o nome do usuário para editar: ")
    if nome_usuario not in database.usuarios:
        print("❌ Usuário não encontrado.")
        return
        
    print(f"Editando usuário: {nome_usuario}")
    usuario = database.usuarios[nome_usuario]

    novo_email = input(f"Novo e-mail ({usuario['email']}): ") or usuario["email"]
    novo_perfil = (
        input(f"Novo perfil ({usuario['perfil']}): ").lower() or usuario["perfil"]
    )
    if novo_perfil not in ["admin", "user"]:
        print("❌ Perfil inválido. Use 'admin' ou 'user'.")
        return

    usuario.update({"email": novo_email, "perfil": novo_perfil})
    database.salvar_dados()
    print(f"\n✅ Usuário '{nome_usuario}' atualizado com sucesso!")


def editar_senha_usuario():
    print("\n--- Alterar Senha do Usuário ---")
    if not auth.usuario_logado:
        print("❌ Nenhum usuário logado.")
        return
        
    print(f"Alterando senha para o usuário: {auth.usuario_logado}")
    senha_atual = getpass("Digite sua senha atual: ")
    
    if database.usuarios[auth.usuario_logado]["senha"] != utils.gerar_hash(senha_atual):
        print("\n❌ Senha atual incorreta.")
        return
        
    nova_senha = getpass("Digite a nova senha: ")
    confirmar_senha = getpass("Confirme a nova senha: ")
    
    if nova_senha != confirmar_senha:
        print("\n❌ As senhas não coincidem.")
        return
    if not nova_senha:
        print("\n❌ A nova senha não pode ser vazia.")
        return
        
    database.usuarios[auth.usuario_logado]["senha"] = utils.gerar_hash(nova_senha)
    database.salvar_dados()
    print(f"\n✅ Senha do usuário '{auth.usuario_logado}' alterada com sucesso!")


def remover_usuario():
    print("\n--- Remover Usuário ---")
    listar_usuarios()
    if not database.usuarios:
        return
    nome_usuario = input("\nDigite o nome do usuário para remover: ")
    if nome_usuario not in database.usuarios:
        print("❌ Usuário não encontrado.")
        return
    if nome_usuario == auth.usuario_logado:
        print("❌ Não é possível remover o usuário atualmente logado.")
        return

    if database.usuarios[nome_usuario]["perfil"] == "admin":
        total_admins = sum(1 for u in database.usuarios.values() if u["perfil"] == "admin")
        if total_admins <= 1:
            print("❌ Não é possível remover o último administrador do sistema.")
            return

    email_usuario = database.usuarios[nome_usuario]["email"]
    del database.usuarios[nome_usuario]
    database.salvar_dados()

    corpo_email = f"""
    <h3>Conta Removida - Sistema Meu Querido Pet</h3>
    <p>Olá, {nome_usuario}!</p>
    <p>Informamos que sua conta foi removida do sistema Meu Querido Pet.</p>
    <p>Você não possui mais acesso ao sistema. Caso isso seja um erro, entre em contato com o administrador.</p>
    <p>Atenciosamente,</p>
    <p>Equipe Meu Querido Pet</p>
    """
    notifications.enviar_email(email_usuario, "Conta Removida - Meu Querido Pet", corpo_email)

    print(f"\n✅ Usuário '{nome_usuario}' removido com sucesso!")


def recuperar_senha_db():
    """Função separada para interagir com DB (usada pelo main)"""
    conn = database.get_conn()
    cur = conn.cursor(dictionary=True)

    email_digitado = input("Digite o e-mail cadastrado para recuperação: ")

    cur.execute("SELECT usuario FROM usuarios WHERE email = %s", (email_digitado,))
    row = cur.fetchone()

    if row is None:
        print("❌ E-mail não encontrado em nosso sistema.")
        conn.close()
        return

    nome_usuario = row["usuario"]
    caracteres = string.ascii_letters + string.digits
    nova_senha_temporaria = "".join(random.choice(caracteres) for _ in range(8))

    cur.execute(
        "UPDATE usuarios SET senha = %s WHERE usuario = %s",
        (utils.gerar_hash(nova_senha_temporaria), nome_usuario),
    )
    conn.commit()
    conn.close()
    
    # Atualiza a senha na memória também, se o programa continuar rodando
    if nome_usuario in database.usuarios:
        database.usuarios[nome_usuario]["senha"] = utils.gerar_hash(nova_senha_temporaria)

    corpo_email = f"""
    <h3>Recuperação de Senha - Sistema Meu Querido Pet</h3>
    <p>Olá, {nome_usuario}!</p>
    <p>Você solicitou a redefinição de sua senha.</p>
    <p>Sua nova senha temporária é: <b>{nova_senha_temporaria}</b></p>
    <p>Recomendamos que você altere esta senha após fazer o login.</p>
    <p>Atenciosamente,</p>
    <p>Equipe Meu Querido Pet</p>
    """
    notifications.enviar_email(email_digitado, "Recuperação de Senha - Meu Querido Pet", corpo_email)
    print("\n✅ Se o e-mail estiver correto, uma nova senha foi enviada para ele.")