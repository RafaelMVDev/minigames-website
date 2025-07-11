from flask import Flask, render_template, request, redirect, url_for, make_response,session

app = Flask(__name__)

USUARIO_CADASTRADO = "admin"
SENHA_CADASTRADA = "123"
NOTICIAS = {'esportes':
            [
                ["https://g1.globo.com/go/goias/videos-ja-1-edicao/video/musica-e-esportes-tomam-conta-das-praias-do-araguaia-13747328.ghtml",'esporte praia toma conta'],
                ['https://ge.globo.com/sportv/','Sportv Notícias'],
                ['https://ge.globo.com/','Globo Esportes']
            ],
            'entretenimento':
            [ 
                ['https://poki.com/br#utm_source=redirect-en-pt','Poki Games'],
                ['https://agar.io','Agar.io'],
                ['https://store.steampowered.com/?l=portuguese','Steam']
            ],
            'lazer':[
                ['https://www.otempo.com.br/pets/10-brincadeiras-para-fazer-com-o-seu-cachorro-1.3058076','Bricandeiras com o Cachorro'],
                ['https://www.netflix.com/br/','Netflix'],
                ['https://pointer.com.br/blog/ferias-em-casa/','Férias em Casa']
            ]}
ORDEM_NOTICIAS = ['esportes', 'entretenimento', 'lazer']
app.secret_key = 'oleoleolaotimaovaiganhar'

@app.route('/noticias')
def noticias():
    noticia = request.form.get('noticia')

    return render_template('noticias.html', noticias = NOTICIAS,noticias_ordem = ORDEM_NOTICIAS)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = ""

    usuario = request.cookies.get("username")
    if request.method == "POST":

        usuario = request.form['username']
        senha = request.form['password']

        if usuario == USUARIO_CADASTRADO and senha == SENHA_CADASTRADA:
            resposta = make_response(redirect(url_for('bemvindo')))
            resposta.set_cookie('username', usuario, max_age=60*10)
            session["visualizacoes"] = 0
            return resposta
        else:
            mensagem = "Usuário ou senha inválidos. Tente novamente."

   
    if usuario:
        return redirect(url_for('bemvindo'))
    return render_template('login.html', error=mensagem, )

@app.route('/bemvindo', methods=["POST", "GET"])
def bemvindo():
    username = request.cookies.get('username')

    if not username:
        return redirect(url_for('login'))
    
    # mudando a cor da página

    tema = request.cookies.get('theme')
    if not tema:
        tema = 'tema_claro'
    print("OII")
    if request.method == "POST":
        tema = request.form.get('tema')
        resposta = make_response(redirect(url_for('bemvindo')))
        resposta.set_cookie('theme', tema,expires = 60 * 30)
        return resposta
    session["visualizacoes"] += 1

    

    return render_template('bemvindo.html', user=username, tema = tema,contador = session["visualizacoes"])


@app.route('/logout')
def logout():
    resposta = make_response(redirect(url_for('login')))

    resposta.set_cookie('username', '', expires=0)

    return resposta

if __name__ == '__main__':
    app.run(debug = True)