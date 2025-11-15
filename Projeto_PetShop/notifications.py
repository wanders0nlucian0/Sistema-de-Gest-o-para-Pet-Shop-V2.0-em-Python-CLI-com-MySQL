import email.message
import smtplib
import telebot

# Importa as configurações e o estado de autenticação
import config
import auth

# ======================================================================
# INICIALIZAÇÃO DO BOT
# ======================================================================
try:
    bot = telebot.TeleBot(config.BOT_TOKEN)
except Exception as e:
    print(f"❌ Erro ao inicializar o bot do Telegram: {e}")
    bot = None # Define como None para evitar falhas

# ======================================================================
# FUNÇÕES DE E-MAIL
# ======================================================================

def enviar_email(destinatario, assunto, corpo_email):
    msg = email.message.EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = config.EMAIL_REMETENTE
    msg["To"] = destinatario
    msg.set_content(corpo_email, subtype="html")
    try:
        print("\nConectando ao servidor de e-mail...")
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(config.EMAIL_REMETENTE, config.SENHA_APP_REMETENTE)
            s.send_message(msg)
        print(f"✅ E-mail enviado com sucesso para {destinatario}!")
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Erro de autenticação: verifique o e-mail ou a senha de app em 'config.py'.")
    except Exception as e:
        print(f"\n❌ Erro ao enviar e-mail: {e}")

# ======================================================================
# FUNÇÕES DE TELEGRAM
# ======================================================================

def _enviar_msg_telegram(mensagem):
    """Função interna para enviar mensagens, tratando erros."""
    if not bot:
        print("❌ Bot do Telegram não inicializado. Notificação pulada.")
        return
    try:
        bot.send_message(config.CHAT_ID, mensagem, parse_mode="Markdown")
        print("✅ Notificação enviada para o Telegram!")
    except Exception as e:
        print(f"❌ Erro ao enviar notificação para o Telegram: {e}")


def enviar_notificacao_venda(itens, total):
    usuario = auth.usuario_logado if auth.usuario_logado else "Sistema"
    mensagem = f"""
🛒 *Nova Venda Registrada!*

👤 *Vendedor:* {usuario}
📋 *Itens:*
"""
    for item in itens:
        mensagem += (
            f"- {item['nome']} ({item['tipo'].capitalize()}): "
            f"{item['quantidade']} x R${item['preco_unitario']:.2f} = "
            f"R${item['subtotal']:.2f}\n"
        )
    mensagem += f"""
💰 *Total:* R${total:.2f}

---
*Meu Querido Pet - Sistema de Gestão*
    """
    _enviar_msg_telegram(mensagem)


def enviar_notificacao_cancelamento_venda(itens, total):
    usuario = auth.usuario_logado if auth.usuario_logado else "Sistema"
    mensagem = f"""
❌ *Venda Cancelada!*

👤 *Responsável:* {usuario}
📋 *Itens:*
"""
    for item in itens:
        mensagem += (
            f"- {item['nome']} ({item['tipo'].capitalize()}): "
            f"{item['quantidade']} x R${item['preco_unitario']:.2f} = "
            f"R${item['subtotal']:.2f}\n"
        )
    mensagem += f"""
💰 *Total:* R${total:.2f}

---
*Meu Querido Pet - Sistema de Gestão*
    """
    _enviar_msg_telegram(mensagem)


def enviar_notificacao_agendamento(tutor, pet, servico, data, hora):
    usuario = auth.usuario_logado if auth.usuario_logado else "Sistema"
    mensagem = f"""
📅 *Novo Agendamento Registrado!*

👤 *Responsável:* {usuario}
👨‍👩‍👧 *Tutor:* {tutor}
🐶 *Pet:* {pet}
🛠 *Serviço:* {servico}
📆 *Data:* {data}
⏰ *Hora:* {hora}

---
*Meu Querido Pet - Sistema de Gestão*
    """
    _enviar_msg_telegram(mensagem)


def enviar_notificacao_cancelamento_agendamento(tutor, pet, servico, data, hora):
    usuario = auth.usuario_logado if auth.usuario_logado else "Sistema"
    mensagem = f"""
❌ *Agendamento Cancelado!*

👤 *Responsável:* {usuario}
👨‍👩‍👧 *Tutor:* {tutor}
🐶 *Pet:* {pet}
🛠 *Serviço:* {servico}
📆 *Data:* {data}
⏰ *Hora:* {hora}

---
*Meu Querido Pet - Sistema de Gestão*
    """
    _enviar_msg_telegram(mensagem)


def enviar_notificacao_estoque(nome_produto, quantidade):
    if quantidade <= 5:
        status = "Baixo (Atenção: Estoque Crítico!)"
    elif quantidade >= 30:
        status = "Alto (Estoque Excedente)"
    else:
        return
    mensagem = f"""
⚠️ *Alerta de Estoque!*

🐕 *Produto:* {nome_produto}
📦 *Quantidade Atual:* {quantidade}
📊 *Status:* {status}

---
*Meu Querido Pet - Sistema de Gestão*
    """
    _enviar_msg_telegram(mensagem)