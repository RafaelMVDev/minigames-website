from flask import Flask, render_template, request, session, redirect, url_for
from json import loads,load
from logica_jogos.jokenpo import Jokenpo
import random
import secrets

jk = Jokenpo()

def inicializar_jokenpo():
    session["pts_player"] = 0
    session["pts_bot"] = 0
    session["escolha_player"] = ''
    session["escolha_bot"] = ''
    session["placar"] = "0x0"
    session["mensagem_aviso"] = ''
    session["cor_aviso"] = ''


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def validar_escolha(escolha):
    if escolha in ['pedra','papel','tesoura']:
        return escolha
    return False



# rota cuida tanto do botao jogar, quanto o botao de selecionar uma escolha
@app.route("/jokenpo",methods=['GET', 'POST'])
def jokenpo():
    if not session.get('placar'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         inicializar_jokenpo()
    if request.method == "POST":
        acao = request.form.get("acao_jogo")
        if acao == "jogar": #botão que mandou a requisição tem o value de jogar, portanto, o botao jogar foi clicado
            escolha_bot = jk.escolherAleatorio()
            
            session["escolha_bot"] = escolha_bot
            resultado = jk.validarVencedorRodada(session.get("escolha_player"),escolha_bot)
           
            # resultado retorna, 'player','bot' ou 'empate', por isso ja uso ele pra alterar a pontuação
            if resultado != 'empate':
                session["cor_aviso"] = resultado+'_ganhou'
                session[f"pts_{resultado}"] += 1
                session["mensagem_aviso"] = resultado.capitalize()+' venceu!' #concatenação simples
                # se o ponto foi feito, validamos o vencedor do jogo
                if jk.validarVencedorJogo(session.get("pts_player"),session.get("pts_bot")) != 'continuar':
                    inicializar_jokenpo()
                    return render_template('pedra_papel_tesoura.html')

            else:
                session["cor_aviso"] = 'empate'
                session["mensagem_aviso"] = 'Empate!' # exibir mensagem diferente se ele perder
            return render_template('pedra_papel_tesoura.html', 
                            imagem_p= url_for('static',filename = f'jokenpo/{session.get("escolha_player")}_img.png'),
                            imagem_b= url_for('static',filename = f'jokenpo/{session.get('escolha_bot')}_img.png'),
                            placar = jk.formatarPlacar(session.get('pts_player'),session.get('pts_bot')),
                            mensagem_aviso = session.get('mensagem_aviso'),
                            cor_aviso = session.get('cor_aviso'))
        else:
            escolha = jk.validarEscolha(acao)
            if escolha:
                session["escolha_player"] = escolha
                
            return render_template('pedra_papel_tesoura.html', 
                            imagem_p= url_for('static',filename = f'jokenpo/{session.get("escolha_player")}_img.png'),
                            imagem_b= url_for('static',filename = ''),
                            placar = jk.formatarPlacar(session.get('pts_player'),session.get('pts_bot')),
                            mensagem_aviso = session.get('mensagem_aviso'),
                            cor_aviso = session.get('cor_aviso'))
    else:
        return render_template('pedra_papel_tesoura.html', 
                            imagem_p= url_for('static',filename = f'jokenpo/{session.get("escolha_player")}_img.png'),
                            imagem_b= url_for('static',filename = ''),
                            placar = jk.formatarPlacar(session.get('pts_player'),session.get('pts_bot')),
                            mensagem_aviso = session.get('mensagem_aviso'),
                            cor_aviso = session.get('cor_aviso'))


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forca")
def forca():
    return render_template('jogo_forca.html')

if __name__ == 'main':
    app.run(debug = True)
   