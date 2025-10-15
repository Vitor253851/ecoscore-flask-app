# registro.py

import datetime
from storage import carregar_registros, salvar_registros
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from utils import score # Importa a função de formatação

def coletar_e_pontuar_habitos_diarios(usuario):
    """
    Apresenta o formulário, coleta as respostas, calcula a pontuação e salva o registro.
    """
    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
    todos_registros = carregar_registros()

    # Verifica se o usuário já preencheu hoje
    registros_usuario = [r for r in todos_registros if r['nome_usuario'] == usuario]
    if any(r['data'] == data_hoje for r in registros_usuario):
        print(f"\n🚫 Você já preencheu o registro para a data {data_hoje}.")
        return

    print("\n" + "="*40)
    print(f"FORMULÁRIO ECOSCORE - {data_hoje}")
    print("Preencha seus hábitos de hoje para receber sua pontuação.")
    print("="*40)

    respostas_diarias = {}
    pontuacao_total = 0

    # Itera sobre cada categoria e pergunta as opções
    for categoria in CATEGORIAS:
        opcoes = PONTUACAO_ECOSCORE[categoria]
        opcoes_lista = list(opcoes.keys())
        
        print(f"\n[{categoria}]:")
        
        # Mostra as opções com números
        for i, opcao in enumerate(opcoes_lista):
            pontos = opcoes[opcao]
            print(f"  [{i+1}] {opcao} ({pontos:+d} pts)")
        
        # Coleta a escolha do usuário
        while True:
            try:
                escolha_indice = int(input(f"Selecione uma opção para {categoria} (1-{len(opcoes_lista)}): ")) - 1
                if 0 <= escolha_indice < len(opcoes_lista):
                    opcao_selecionada = opcoes_lista[escolha_indice]
                    pontos_obtidos = opcoes[opcao_selecionada]
                    
                    # 1. Armazena a resposta
                    respostas_diarias[categoria.lower()] = opcao_selecionada
                    
                    # 2. Calcula a pontuação
                    pontuacao_total += pontos_obtidos
                    
                    print(f"  -> Seleção: '{opcao_selecionada}'. Pontos: {pontos_obtidos:+d}.")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

    # 3. Salva o registro
    novo_registro = {
        "nome_usuario": usuario,
        "data": data_hoje,
        "pontuacao": pontuacao_total,
        **respostas_diarias  # Adiciona as respostas de cada categoria
    }
    
    todos_registros.append(novo_registro)
    salvar_registros(todos_registros)

    print("\n" + "#"*40)
    print(f"🎉 Registro de hoje salvo! Sua pontuação total foi: {pontuacao_total:+d} pontos.")
    print("#"*40)