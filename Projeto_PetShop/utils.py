import hashlib
import os
from datetime import datetime

# ======================================================================
# FUNÇÕES UTILITÁRIAS
# ======================================================================

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_hora(hora_str):
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False