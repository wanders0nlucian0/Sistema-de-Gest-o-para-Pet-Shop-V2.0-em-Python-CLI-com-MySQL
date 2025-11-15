import os
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

PASTA = os.getenv("PASTA_DADOS", "dados_petshop")
os.makedirs(PASTA, exist_ok=True)

# CONFIGURAÇÕES DE E-MAIL
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP_REMETENTE = os.getenv("SENHA_APP_REMETENTE")

# CONFIGURAÇÕES DO BOT DO TELEGRAM
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# CONFIGURAÇÕES DO MYSQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB", "meu_querido_pet")
