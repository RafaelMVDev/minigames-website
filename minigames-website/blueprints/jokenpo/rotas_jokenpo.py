#  =====  Módulos =====
from flask import Blueprint,session,render_template,redirect,url_for,request
from blueprints.jokenpo.logica_jogo.jokenpo import Jokenpo

#  =====  Inicializando objetos =====
jk = Jokenpo()
jk_bp = Blueprint("jokenpo",__name__,template_folder="templates",static_folder= "static")

#  =====  Funções =====
def inicializar_jokenpo() -> ():  
    session["jokenpo"] = {}
    session["jokenpo"]["pts_player"] = 0
    session["jokenpo"]["pts_bot"] = 0
    session["jokenpo"]["escolha_player"] = ''
    session["jokenpo"]["escolha_player_url"] = ''
    session["jokenpo"]["escolha_bot"] = ''
    session["jokenpo"]["escolha_bot_url"] = ''
    session["jokenpo"]["placar"] = "0x0"
    session["jokenpo"]["mensagem_aviso"] = ''
    session["jokenpo"]["cor_aviso"] = ''

# rota cuida tanto do botao jogar, quanto o botao de selecionar uma escolha

@jk_bp.route("",methods=['GET', 'POST'])
def jokenpo():
    print("oi")
    if not session.get('jokenpo'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         inicializar_jokenpo()
    jokenpo_data = session.get("jokenpo")
    if request.method == "POST":
        jokenpo_data = session.get("jokenpo")
        dados = request.get_json() #aqui eu acesso os dados mandadados do client
        escolha_p = jk.validarEscolha(dados.get("escolha_player"))
        escolha_bot = jk.escolherAleatorio()

        jokenpo_data["escolha_player"] = escolha_p
        jokenpo_data["escolha_player_url"] = url_for('jokenpo.static',filename = f'{jokenpo_data["escolha_player"]}_img.png')
        escolha_bot = jk.escolherAleatorio()
        jokenpo_data["escolha_bot"] = escolha_bots
        jokenpo_data["escolha_bot_url"] = url_for('jokenpo.static',filename = f'{jokenpo_data["escolha_bot"]}_img.png')
        
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
        jokenpo_data["escolha_bot_url"] = url_for('jokenpo.static',filename = f'{jokenpo_data["escolha_bot"]}_img.png')
        resposta["escolha_bot_url"] = jokenpo_data["escolha_bot_url"]
        session["jokenpo"] = jokenpo_data
        return resposta # vai ser enviado de volto pro js mostrar pro cliente

    #GET request so é atividado quando  a URL é acessada / página recarregada

    return render_template('jokenpo.html', 
                        imagem_p=  jokenpo_data["escolha_player_url"],
                        imagem_b= jokenpo_data['escolha_bot_url'],
                        placar = jokenpo_data["placar"],
                        mensagem_aviso = jokenpo_data["mensagem_aviso"],
                        cor_aviso = jokenpo_data['cor_aviso'])
