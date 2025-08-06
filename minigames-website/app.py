# ==== Bibliotecas ====
from flask import Flask,jsonify, render_template, request, session, redirect, url_for
from json import loads,load

import random
import secrets

# - Blueprints -
from blueprints.jokenpo.rotas_jokenpo import jk_bp # Jokenpo blueprint
from blueprints.forca.rotas_forca import fc_bp # Forca blueprint
from blueprints.adivinhe_numero.rotas_adivinhar_numero import adv_n_bp # Adivinhar numero blueprint


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Registrando as Blueprints aqui
app.register_blueprint(jk_bp,url_prefix = "/jokenpo")
app.register_blueprint(fc_bp,url_prefix = "/forca")
app.register_blueprint(adv_n_bp,url_prefix = "/adivinhar_numero")

@app.route("/")
def index():
    
    return render_template('index.html')

  

if __name__ == 'main':
    print("WHAT")
    for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, Rule: {rule.rule}")
    app.run(debug = True)

for rule in app.url_map.iter_rules():
    print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, Rule: {rule.rule}")