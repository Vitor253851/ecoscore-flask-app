# utils.py

# Códigos ANSI para cores no terminal
class Cores:
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'

# Funções de formatação
def sucesso(texto):
    return f"{Cores.VERDE}{Cores.BRIGHT}✅ {texto}{Cores.RESET}"

def erro(texto):
    return f"{Cores.VERMELHO}{Cores.BRIGHT}❌ {texto}{Cores.RESET}"

def aviso(texto):
    return f"{Cores.AMARELO}{texto}{Cores.RESET}"

def score(pontos):
    """Formata a pontuação com cor baseada no valor."""
    cor = Cores.VERDE if pontos >= 0 else Cores.VERMELHO
    return f"{cor}{Cores.BRIGHT}{pontos:+d}{Cores.RESET} pts"