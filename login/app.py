from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)

app.secret_key = "rafaeléumcaramuitolegal"

SENHA_USUARIO = "UMCARAMUITOLEGAL123"
produtos = ["banana","maça"]
@app.route("/", methods = ["GET"])
def index():
    if 'username' in session:
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
        if senha == SENHA_USUARIO:
            session["username"] = usuario
            print(session.get("username"))
            return redirect(url_for("home"))
        else:
            return render_template("senha_errada.html")

@app.route('/profile', methods = ["GET"]) 
def profile():
    if request.method == "GET":
        return render_template("perfil.html", user = session.get("username"), produtos = ["banana","maça"])
    else:
        return f'TA ESTRANHO ISSO AE PAIZÃO'

@app.route('/logout', methods = ["GET","POST"])
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug = True)