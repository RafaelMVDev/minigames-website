#  =====  Módulos =====
from flask import Blueprint,session,render_template,redirect,url_for,request
from blueprints.jokenpo.logica_jogo.jokenpo import Jokenpo

#  =====  Inicializando objetos =====
jk = Jokenpo()
jk_bp = Blueprint("jokenpo",__name__,template_folder="templates",static_folder= "static")

def data():
    return session.setdefault("jokenpo", {
        "pts_player": 0,
        "pts_bot": 0,
        "escolha_player": '',
        "escolha_player_url": '',
        "escolha_bot": '',
        "escolha_bot_url": '',
        "placar": "0x0",
        "mensagem_aviso": '',
        "cor_aviso": ''
    })

#  =====  Funções =====
def reinicializar_jokenpo() -> ():  
  
    data()["pts_player"] = 0
    data()["pts_bot"] = 0
    data()["escolha_player"] = ''
    data()["escolha_player_url"] = ''
    data()["escolha_bot"] = ''
    data()["escolha_bot_url"] = ''
    data()["placar"] = "0x0"
    data()["mensagem_aviso"] = ''
    data()["cor_aviso"] = ''

# rota cuida tanto do botao jogar, quanto o botao de selecionar uma escolha
# Com base na escolha do player, realiza a rodada 
def efetuar_rodada(escolha_player):
    data()["escolha_player"] = escolha_player
    data()["escolha_player_url"] = url_for('jokenpo.static',filename = f'{data()["escolha_player"]}_img.png')
    data()["escolha_bot"] = jk.escolherAleatorio()
    data()["escolha_bot_url"] =  url_for('jokenpo.static',filename = f'{data()["escolha_bot"]}_img.png')

    resultado_rodada = jk.validarVencedorRodada(escolha_player,data()["escolha_bot"])
    if resultado_rodada != "empate":
        data()["cor_aviso"] = resultado_rodada +'_ganhou'
        data()[f"pts_{resultado_rodada}"] += 1
        data()["mensagem_aviso"] = resultado_rodada.capitalize() + ' venceu!' #concatenação simples
        data()["placar"] = jk.formatarPlacar(session["jokenpo"]['pts_player'],session["jokenpo"]['pts_bot'])
    else:
        data()["cor_aviso"] = 'empate'
        data()["mensagem_aviso"] = 'Empate!' # exibir mensagem diferente se ele perder

    
    return resultado_rodada # Retorna o resultado da rodada

@jk_bp.route("",methods=['GET', 'POST'])
def jokenpo():

    if not session.get('jokenpo'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         data() # inicializa a sessao

    if request.method == "POST":

        dados = request.get_json() #aqui eu acesso os dados mandadados do client
        
        escolha_p = jk.validarEscolha(dados.get("escolha_player"))
        efetuar_rodada(escolha_p) # realiza a rodada e atualiza os dados da sessão

        status_jogo = jk.validarVencedorJogo(data()["pts_player"],data()["pts_bot"])
        resposta = {}
        if status_jogo != 'continuar':
            reinicializar_jokenpo()
            resposta["resultado_jogo"] = status_jogo

        session.modified = True
        resposta["escolha_bot_url"] = data()["escolha_bot_url"]
        resposta["mensagem_aviso"] = data()["mensagem_aviso"]
        resposta["cor_aviso"] = data()["cor_aviso"]
        resposta["placar"] = data()["placar"]

        return resposta # vai ser enviado de volta pro js mostrar pro cliente

    #GET request so é atividado quando  a URL é acessada / página recarregada

    return render_template('jokenpo.html', 
                        imagem_p=  data()["escolha_player_url"],
                        imagem_b= data()['escolha_bot_url'],
                        placar = data()["placar"],
                        mensagem_aviso = data()["mensagem_aviso"],
                        cor_aviso = data()['cor_aviso'])
