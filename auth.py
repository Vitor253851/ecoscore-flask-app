# Importa as funções de armazenamento
from storage import carregar_usuarios, salvar_usuarios, carregar_registros, salvar_registros

def cadastro_usuario(nome_usuario, senha):
    """
    Cadastra um novo usuário e o inicializa no sistema de registro.
    Retorna True em sucesso, False se o usuário já existir.
    """
    lista_usuarios = carregar_usuarios()
    # Verifica se o nome de usuário já existe na lista de dicionários
    if any(u['nome_usuario'] == nome_usuario for u in lista_usuarios):
        print(f"\nUsuário '{nome_usuario}' já existe. Tente outro nome.")
        return False
    
    # Adiciona o novo usuário à lista
    novo_usuario = {'nome_usuario': nome_usuario, 'senha': senha}
    lista_usuarios.append(novo_usuario)
    salvar_usuarios(lista_usuarios)
    
    print(f"\n✅ Usuário '{nome_usuario}' cadastrado com sucesso!")
    # Não é mais necessário inicializar registros aqui, pois o arquivo é uma lista única
    return True

def login_usuario(nome_usuario, senha):
    """
    Verifica se o usuário e a senha estão corretos.
    Retorna o nome_usuario em sucesso, None em falha.
    """
    lista_usuarios = carregar_usuarios()
    usuario_encontrado = None
    
    # 1. Procura o usuário na lista
    for u in lista_usuarios:
        if u.get('nome_usuario') == nome_usuario:
            usuario_encontrado = u
            break
            
    if not usuario_encontrado:
        print("\n❌ Login falhou: Usuário não encontrado.")
        return None
        
    # 2. Se encontrou, verifica a senha
    if usuario_encontrado['senha'] == senha:
        print(f"\nBem-vindo(a) de volta, {nome_usuario}!")
        return nome_usuario
    else:
        print("\n❌ Login falhou: Senha incorreta.")
        return None

# # Para testar as funções (remova ou comente após o teste)
# if __name__ == '__main__':
#     # Teste de Cadastro
#     cadastro_usuario("teste_novo", "123")
#     
#     # Teste de Login (sucesso)
#     usuario_logado = login_usuario("teste_novo", "123")
#     print(f"Status Login: {usuario_logado}")
#     
#     # Teste de Login (falha)
#     usuario_falho = login_usuario("teste_novo", "999")
#     print(f"Status Login: {usuario_falho}")