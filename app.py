# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
from auth import cadastro_usuario, login_usuario
from storage import carregar_registros, salvar_registros
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from desempenho import get_dados_desempenho, get_dica_personalizada

app = Flask(__name__)
# Chave secreta necessária para usar 'flash messages' (notificações)
app.secret_key = 'uma-chave-secreta-muito-segura-e-dificil-de-adivinhar' 

@app.route('/')
def index():
    """Página inicial: redireciona para o login ou para o menu principal."""
    if 'usuario' in session:
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        
        usuario = login_usuario(nome, senha)
        if usuario:
            session['usuario'] = usuario # Armazena o usuário na sessão
            flash(f'Bem-vindo(a) de volta, {usuario}!', 'success')
            return redirect(url_for('menu'))
        else:
            # A função login_usuario já imprime o erro no console.
            # Para a web, seria melhor retornar a mensagem para o template.
            flash('Usuário ou senha inválidos.', 'danger')
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        
        if cadastro_usuario(nome, senha):
            flash('Usuário cadastrado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Nome de usuário já existe. Tente outro.', 'warning')

    return render_template('cadastro.html')

@app.route('/menu')
def menu():
    if 'usuario' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('menu.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None) # Remove o usuário da sessão
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

# --- Rotas para as funcionalidades principais (placeholders) ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']
    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
    
    # Verifica se o usuário já preencheu o formulário hoje
    todos_registros = carregar_registros()
    registros_usuario = [r for r in todos_registros if r.get('nome_usuario') == usuario]
    ja_registrou = any(r.get('data') == data_hoje for r in registros_usuario)

    if request.method == 'POST':
        if ja_registrou:
            flash('Você já registrou seus hábitos hoje.', 'warning')
            return redirect(url_for('menu'))

        respostas_diarias = {}
        pontuacao_total = 0

        # Coleta as respostas do formulário e calcula a pontuação
        for categoria in CATEGORIAS:
            # O nome do campo no formulário é a categoria em minúsculas
            chave_categoria = categoria.lower()
            opcao_selecionada = request.form.get(chave_categoria)
            
            if opcao_selecionada:
                respostas_diarias[chave_categoria] = opcao_selecionada
                pontuacao_total += PONTUACAO_ECOSCORE[categoria][opcao_selecionada]

        # Salva o novo registro
        novo_registro = {
            "nome_usuario": usuario,
            "data": data_hoje,
            "pontuacao": pontuacao_total,
            **respostas_diarias
        }
        todos_registros.append(novo_registro)
        salvar_registros(todos_registros)

        flash(f'🎉 Registro salvo! Sua pontuação de hoje foi: {pontuacao_total:+d} pontos.', 'success')
        return redirect(url_for('menu'))

    # Se for GET, exibe o formulário ou a mensagem de que já registrou
    return render_template('registro.html', categorias=PONTUACAO_ECOSCORE, ja_registrou=ja_registrou)

@app.route('/desempenho')
def desempenho():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    dados = get_dados_desempenho(usuario)

    # Passa os dados para o template. Se 'dados' for None, o template tratará disso.
    return render_template('desempenho.html', dados=dados)



@app.route('/dicas')
def dicas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    dica = get_dica_personalizada(usuario)
    
    return render_template('dicas.html', dica=dica)

# Roda o servidor de desenvolvimento
if __name__ == '__main__':
    # O modo debug reinicia o servidor automaticamente a cada alteração no código.
    app.run()
