#  =====  Módulos =====
from flask import Blueprint,session,render_template,redirect,url_for,request
from blueprints.forca.logica_jogo.forca import Forca

#  =====  Inicializando objetos =====
fc = Forca()
fc_bp = Blueprint("forca",__name__,template_folder="templates",static_folder= "static")

def inicializar_forca():
    session["forca"] = {}
    session["forca"]["erros"] = 0
    session["forca"]["palavra_escolhida"] = fc.palavraAleatoria() 
    session["forca"]["letras_descobertas"] = '_'* len(session["forca"])

@fc_bp.route("/forca", methods = ["GET","POST"])
def forca():
     
    if not session.get('forca'): # inicializa as variaveis da sessão logo que a primeira requisição é feita
         inicializar_forca()
         
    if request.method == "POST":
        
        forca_data = session.get("forca")
        print(forca_data)
        dados = request.get_json() #aqui eu acesso os dados mandadados do client
        escolha_p = fc.validarEscolha(dados.get("escolha_player"))
        estado_palavra = fc.checarLetraForca(forca_data["palavra_escolhida"],forca_data["letras_descobertas"],escolha_p)
        resposta = {}

        if forca_data["letras_descobertas"] != estado_palavra:
             forca_data["letras_descobertas"] = estado_palavra
        else:
            forca_data["erros"] += 1
    
        resposta["erros"] = forca_data["erros"]
        resposta["nova_palavra"] = forca_data["letras_descobertas"]
      
        return resposta # vai ser enviado de volto pro js mostrar pro cliente

    #GET request so é atividado quando  a URL é acessada / página recarregada
    jokenpo_data = session.get("jokenpo")
    return render_template('jogo_forca.html')
