from flask import Flask, session, redirect, url_for, request, render_template, make_response

app = Flask(__name__)

app.secret_key = "rafaeléumcaramuitolegal"
NOME_USUARIO = "moravi"
SENHA_USUARIO = "1234"
produtos = ["banana","maça"]
@app.route("/", methods = ["GET"])
def index():
    user = request.cookies.get("username")
    if user:
        print("TEM SESSÃO!")
        return redirect(url_for("home"))
       
    return redirect(url_for("login"))

@app.route("/home",methods = ["GET","POST"])
def home():
    if request.method == "POST":
        return render_template("home.html", produtos = produtos)
    else:
        return render_template("home.html", produtos = produtos)
    
@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/login_validation",methods = ["GET","POST"])
def login_validation():
    if request.method == "POST":
        usuario =  request.form.get("usuario")
        senha  = request.form.get("senha")
        if usuario == NOME_USUARIO and senha == SENHA_USUARIO:
            resposta = make_response(redirect(url_for('home')))
            resposta.set_cookie('username', usuario, max_age = 60 *10)
            session["username"] = usuario
            print(session.get("username"))
            return resposta
        else:
            return render_template("senha_errada.html")

@app.route('/profile', methods = ["GET"]) 
def profile():
    usuario = request.cookies.get('username')
    print(usuario)
    if not usuario:
        return redirect(url_for('login'))
    return render_template("perfil.html", user = session.get("username"), produtos = ["banana","maça"])
    

@app.route('/logout', methods = ["GET","POST"])
def logout():
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username','',expires=0)
    session.pop("username",None)
    return resposta



if __name__ == "__main__":
    app.run(debug = True)