from flask import Flask,jsonify, render_template, request, session, redirect, url_for
from json import loads,load
from logica_jogos.jokenpo import Jokenpo
import random
import secrets

jk = Jokenpo()

def inicializar_jokenpo():
    session["jokenpo"] = {}
    session["jokenpo"]["pts_player"] = 0
    session["jokenpo"]["pts_bot"] = 0
    session["jokenpo"]["escolha_player"] = ''
    session["jokenpo"]["escolha_bot"] = ''
    session["jokenpo"]["placar"] = "0x0"
    session["jokenpo"]["mensagem_aviso"] = ''
    session["jokenpo"]["cor_aviso"] = ''


def validar_escolha(escolha):
    if escolha in ['pedra','papel','tesoura']:
        return escolha
    return False

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# rota cuida tanto do botao jogar, quanto o botao de selecionar uma escolha
@app.route("/jokenpo",methods=['GET', 'POST'])
def jokenpo():
    
    if not session.get('jokenpo'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         inicializar_jokenpo()
         
    if request.method == "POST":
        jokenpo_data = session.get("jokenpo")
        dados = request.get_json() #aqui eu acesso os dados mandadados do client
        escolha_p = jk.validarEscolha(dados.get("escolha_player"))
        jokenpo_data["escolha_player"] = escolha_p
        escolha_bot = jk.escolherAleatorio()
            
        jokenpo_data["escolha_bot"] = escolha_bot
        resultado = jk.validarVencedorRodada(jokenpo_data["escolha_player"],escolha_bot)
        resposta = {}
        # resultado retorna, 'player','bot' ou 'empate', por isso ja uso ele pra alterar a pontuação
        if resultado != 'empate':

            jokenpo_data["cor_aviso"] = resultado+'_ganhou'
            jokenpo_data[f"pts_{resultado}"] += 1
            jokenpo_data["mensagem_aviso"] = resultado.capitalize()+' venceu!' #concatenação simples
            jokenpo_data["placar"] = jk.formatarPlacar(jokenpo_data['pts_player'],jokenpo_data['pts_bot'])
            # se o ponto foi feito, validamos o vencedor do jogo
            resultado = jk.validarVencedorJogo(jokenpo_data["pts_player"],jokenpo_data["pts_bot"])
            if resultado != 'continuar':
                inicializar_jokenpo()
                resposta["resultado_jogo"] =resultado 
        else:
            jokenpo_data["cor_aviso"] = 'empate'
            jokenpo_data["mensagem_aviso"] = 'Empate!' # exibir mensagem diferente se ele perder

        session.modified = True
    
        resposta["mensagem_aviso"] = jokenpo_data["mensagem_aviso"]
        resposta["cor_aviso"] = jokenpo_data["cor_aviso"]
        resposta["placar"] = jokenpo_data["placar"]
        resposta["escolha_bot"] = jokenpo_data["escolha_bot"]
       
        return resposta # vai ser enviado de volto pro js mostrar pro cliente

    #GET request so é atividado quando  a URL é acessada / página recarregada
    jokenpo_data = session.get("jokenpo")
    return render_template('jokenpo.html', 
                        imagem_p= url_for('static',filename = f'jokenpo/{ jokenpo_data["escolha_player"]}_img.png'),
                        imagem_b= url_for('static',filename = f'jokenpo/{jokenpo_data['escolha_bot']}_img.png'),
                        placar = jokenpo_data["placar"],
                        mensagem_aviso = jokenpo_data["mensagem_aviso"],
                        cor_aviso = jokenpo_data['cor_aviso'])



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forca")
def forca():
    return render_template('jogo_forca.html')

if __name__ == 'main':
    app.run(debug = True)
   