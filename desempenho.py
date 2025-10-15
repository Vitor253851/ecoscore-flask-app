# desempenho.py

from storage import carregar_registros
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from collections import defaultdict

# --- BASE DE DICAS ---

DICAS = {
    "TRANSPORTE": "Se seu score em Transporte está baixo, que tal planejar uma 'Segunda de Carona' ou testar o transporte público? Cada viagem conta!",
    "RESIDUOS": "Separe seu lixo orgânico do reciclável. Se já recicla, o próximo passo é a compostagem! Isso melhora muito seu score.",
    "ENERGIA": "Verifique os 'vampiros de energia': retire carregadores da tomada quando não estiverem em uso e desligue o monitor do PC. Pequenos gestos, grandes pontos!",
    "ALIMENTACAO": "Reduza o consumo de carne vermelha. Tente incluir uma refeição vegetariana ou vegana por dia para um grande impacto no seu EcoScore."
}


# ... (código anterior da base de dicas)

def analisar_pior_categoria(historico):
    """
    Analisa o último registro para encontrar a categoria de pior pontuação no dia.
    Isso é usado para personalizar a dica.
    """
    if not historico:
        return None

    ultimo_registro = historico[-1] # O registro já é um dicionário plano
    pior_categoria = None
    pior_pontuacao = float('inf')

    # Percorre as escolhas do último dia e busca a pontuação na matriz
    # Itera apenas sobre as categorias de hábitos, ignorando outras chaves como 'data' ou 'pontuacao'
    for categoria_upper in CATEGORIAS:
        try:
            categoria_lower = categoria_upper.lower()
            resposta = ultimo_registro.get(categoria_lower)
            if resposta is None: continue # Pula se a categoria não estiver no registro

            pontuacao_escolha = PONTUACAO_ECOSCORE[categoria_upper][resposta]

            if pontuacao_escolha < pior_pontuacao:
                pior_pontuacao = pontuacao_escolha
                pior_categoria = categoria_upper
        except KeyError:
            # Se a chave não existir na configuração, ignora
            continue

    return pior_categoria

def get_dados_desempenho(usuario):
    """
    Calcula os dados de desempenho para um usuário e retorna um dicionário.
    Ideal para uso em aplicações web.
    """
    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r.get('nome_usuario') == usuario]

    if not historico:
        return None

    # Garante que o histórico esteja ordenado pela data
    historico_ordenado = sorted(historico, key=lambda r: r.get('data', ''))

    total_dias = len(historico_ordenado)
    pontuacao_total = sum(r['pontuacao'] for r in historico_ordenado)
    media_diaria = pontuacao_total / total_dias if total_dias > 0 else 0

    # Prepara os dados para o gráfico
    # Pega os últimos 30 registros para não poluir o gráfico
    historico_grafico = historico_ordenado[-30:]
    chart_labels = [r.get('data', '') for r in historico_grafico]
    chart_data = [r.get('pontuacao', 0) for r in historico_grafico]

    return {
        'pontuacao_total': pontuacao_total,
        'media_diaria': media_diaria,
        'historico_recente': historico_ordenado[-5:], # Pega os últimos 5 para a tabela
        'chart_labels': chart_labels,
        'chart_data': chart_data
    }

def get_dica_personalizada(usuario):
    """
    Analisa o último registro do usuário e retorna uma dica personalizada em um dicionário.
    """
    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r.get('nome_usuario') == usuario]

    if not historico:
        return {
            'titulo': "Comece sua jornada!",
            'texto': "Você ainda não possui registros. Preencha o formulário de hábitos para começar a receber dicas personalizadas."
        }

    # Garante que o histórico esteja ordenado para pegar o último registro
    historico_ordenado = sorted(historico, key=lambda r: r.get('data', ''))
    ultimo_registro = historico_ordenado[-1]
    pior_categoria = analisar_pior_categoria(historico_ordenado)

    # Verifica se a pontuação da pior categoria foi de fato negativa
    if pior_categoria:
        try:
            pior_pontuacao = PONTUACAO_ECOSCORE[pior_categoria][ultimo_registro[pior_categoria.lower()]]
            if pior_pontuacao < 0:
                return {
                    'titulo': f"💡 Foco em: {pior_categoria.title()}",
                    'texto': DICAS.get(pior_categoria, "Continue se esforçando! Cada pequena ação conta.")
                }
        except KeyError:
            pass # Ignora caso haja alguma inconsistência nos dados

    # Mensagem padrão se todas as pontuações do último dia foram positivas
    return {
        'titulo': "✨ Parabéns!",
        'texto': "Seu último registro foi excelente! Continue com os bons hábitos. Um ótimo desafio é tentar manter essa performance por uma semana inteira."
    }

def exibir_desempenho(usuario):
    """Calcula e exibe a pontuação total, a média e o histórico recente do usuário."""

    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r['nome_usuario'] == usuario]

    if not historico:
        print("\nℹ️ Você ainda não possui registros. Preencha o formulário primeiro!")
        return

    total_dias = len(historico)
    pontuacao_total = sum(registro['pontuacao'] for registro in historico)

    # Cálculo da Média
    media_diaria = pontuacao_total / total_dias if total_dias > 0 else 0

    print("\n" + "💰"*20)
    print(f"RESUMO DE DESEMPENHO DE {usuario.upper()}")
    print("💰"*20)
    print(f"Período Total Registrado: {total_dias} dias")
    print(f"Pontuação Total Acumulada: {pontuacao_total:+d} pontos")
    print(f"Média Diária (EcoScore): {media_diaria:.2f} pontos")

    print("\nÚLTIMOS REGISTROS (5 dias):")
    # Exibe os 5 registros mais recentes
    for i, registro in enumerate(historico[-5:]):
        print(f"  {i+1}. Data: {registro['data']} | Pontos: {registro['pontuacao']:+d}")

    # Retorna o resultado da análise para ser usado na função de dicas
    return analisar_pior_categoria(historico)


# ... (código anterior)

def gerar_dicas(usuario):
    """Gera uma dica personalizada com base na categoria de pior desempenho recente."""

    # Chamamos exibir_desempenho para mostrar o resumo e obter a análise
    pior_categoria = exibir_desempenho(usuario)

    if pior_categoria is None:
        return

    # Se a pior pontuação for zero ou positiva, o usuário está indo bem!
    if pior_categoria is not None:
        try:
            # Verifica se o pior_pontuacao obtido na função anterior é negativo
            todos_registros = carregar_registros()
            historico_usuario = [r for r in todos_registros if r['nome_usuario'] == usuario]
            ultimo_registro = historico_usuario[-1]
            pior_pontuacao = PONTUACAO_ECOSCORE[pior_categoria][ultimo_registro[pior_categoria.lower()]]
            if pior_pontuacao >= 0:
                 print("\n\n✨ Excelente trabalho! Seu último registro foi muito positivo. Aqui está um desafio:")
                 print("⭐ Tente manter todos os hábitos positivos por 7 dias seguidos!")
                 return
        except KeyError:
            pass # Continua para a dica personalizada se houver erro ou pontuação negativa

    print("\n" + "💡"*10)
    print(f"SUGESTÃO DE MELHORIA - FOCO: {pior_categoria}")
    print("💡"*10)

    dica_personalizada = DICAS.get(pior_categoria, "Continue se esforçando! Seu progresso é importante para o planeta.")

    print(dica_personalizada)


    