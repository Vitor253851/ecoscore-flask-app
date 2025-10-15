# config_score.py

# Matriz de Pontuação do EcoScore
# Estrutura: CATEGORIA -> OPÇÃO -> PONTOS

PONTUACAO_ECOSCORE = {
    "TRANSPORTE": {
        "Carro (Sozinho)": -5,
        "Carro (Com carona)": 0,
        "Transporte Público": +5,
        "Bicicleta/A pé": +10,
        "Nenhuma viagem longa": +3  # Bônus por ficar em casa
    },
    "RESIDUOS": {
        "Não reciclei": -3,
        "Separei para reciclagem": +5,
        "Compostei resíduos orgânicos": +7
    },
    "ENERGIA": {
        "Deixei luzes acesas/aparelhos em standby": -2,
        "Desliguei tudo ao sair": +4,
        "Usei energia de forma consciente e desliguei o AC": +6
    },
    "ALIMENTACAO": {
        "Comi carne vermelha": -3,
        "Comi carne branca/ovos": 0,
        "Fui vegetariano/vegano": +5
    }
}

# Lista das categorias para facilitar a iteração no formulário
CATEGORIAS = list(PONTUACAO_ECOSCORE.keys())