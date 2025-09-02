

#  =====  Módulos =====
from flask import Blueprint,session,render_template,redirect,url_for,request
from blueprints.forca.logica_jogo.forca import Forca

#  =====  Inicializando objetos =====
fc = Forca()
fc_bp = Blueprint("forca",__name__,template_folder="templates",static_folder= "static")

def data():
    return session.setdefault("forca",{
        "erros" : 0,
        "palavra_escolhida" : fc.palavraAleatoria() ,
        "letras_descobertas" :"",
        "letras_tentadas" : []
    }
)

def reiniciar_forca():
    data()["erros"] = 0
    data()["palavra_escolhida"] = fc.palavraAleatoria()
    data()["letras_descobertas"] = '_'* len(data()["palavra_escolhida"])
    data()["letras_tentadas"] = []

@fc_bp.route("", methods = ["GET","POST"])
def forca():
     
    if not session.get('forca'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         print("NAO TEM")
         data()
         data()["letras_descobertas"] = "_" * len(data()["palavra_escolhida"])
         
    if request.method == "POST":
        dados = request.get_json() #aqui eu acesso os dados mandados do cliente
        escolha_p = fc.validarEscolha(dados.get("escolha_player"))
        repetiu_letra = False # podia ter um nome melhor, mas fiquei sem criativade

        if escolha_p not in data()["letras_tentadas"]:  # exibir pro jogador depois ( poderia ser feito no cliente, mas se ele enviar uma letra que ja havia enviado novamente, conto como erro)
            data()["letras_tentadas"].append(escolha_p)
        else:
            repetiu_letra = True # podia ter um nome melhor, mas fiquei sem criativade
            data()["erros"] += 1

        resposta = {}
        resultado_jogo = False
        if not(repetiu_letra): # se  o jogador repetiu letra, nem precisa verificar
            ep,resultado_jogo = fc.analisarTentativa(data()["palavra_escolhida"],data()["letras_descobertas"],escolha_p)
            if resultado_jogo == "acertou_letra" :
                print("Acertou letra!")
                data()["letras_descobertas"] = ep
                resposta["letras_descobertas"] = data()["letras_descobertas"]
            elif resultado_jogo == "errou" :
                data()["erros"] += 1
                resposta["erros"] = data()["erros"]
                if data()["erros"] >= 6:
                    print("perdeu!")
                    resposta["resultado_jogo"] = "perdeu"
            else:   # jogador ganhou nesse caso ( resultado_jogo só pode ser: "acertou", "errou" ou "ganhou")
                print("ganhou!")
                resposta["palavra_original"] = data()["palavra_escolhida"]
                resposta["resultado_jogo"] = "ganhou"
                 # jogador ganhou nesse caso ( resultado_jogo só pode ser: "acertou", "errou" ou "ganhou")

        # desculpa por esse if aqui, mas nao pensei em um jeito melhor de resetar isso sem fazer uma copia dos dados antes
        resposta["letras_tentadas"] = data()["letras_tentadas"]
        resposta["erros"] = data()["erros"]

        if resultado_jogo == "perdeu" or resultado_jogo == "ganhou":
            reiniciar_forca()
        session.modified = True
        return resposta # vai ser enviado de volto pro js mostrar pro cliente

    #GET request so é atividado quando  a URL é acessada / página recarregada

    return render_template('jogo_forca.html')
