import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import Error

app = flask.Flask(__name__)
app.config["DEBUG"] = True

con = mysql.connector.connect(host='localhost', database='teste', user='root', password='m123')

if con.is_connected():
    cursor = con.cursor()
    cursor.execute("select database();")
    cursor.fetchone()

    consulta = "select * from tbl_produtos;"
    cursor.execute(consulta)
    linhas = cursor.fetchall()

    dados = []
    for linha in linhas:
        dado = {}
        dado['Id'] = linha[0]
        dado['Nome'] = linha[1]
        dado['Preco'] = linha[2]
        dado['Quantidade:'] = linha[3]
        dados.append(dado)

    print(dados)
cursor.close()
con.close()

@app.route('/', methods=['GET'])
def home():
    return"<h1>Distant Reading Archive</h1>" \
           "<p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(dados)

app.run()