import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import Error

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#crud
def consulta():
    try:
        con = mysql.connector.connect(host='localhost', database='teste', user='root', password='m123')
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute("select database();")
            cursor.fetchone()

            consulta = "select * from tbl_produtos;"
            cursor.execute(consulta)
            linhas = cursor.fetchall()

            global produtos
            produtos = []
            for linha in linhas:
                produto = {}
                produto['Id'] = linha[0]
                produto['Nome'] = linha[1]
                produto['Preco'] = linha[2]
                produto['Quantidade:'] = linha[3]
                produtos.append(produto)

    except Error as e:
        print("Erro ao acessar a tabela MySQL", e, "\n")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexao com MySQL foi encerrada")

def insere_dados():
    request_data = request.get_json()
    nome = None
    preco = None
    quantidade = None
    if request_data:
        if 'nome' in request_data:
            nome = request_data['nome']
        if 'preco' in request_data:
            preco = request_data['preco']
        if 'quantidade' in request_data:
            quantidade = request_data['quantidade']
    declaracao = '''INSERT INTO tbl_produtos(nome,preco,quantidade)
            VALUES ('''
    dados = f"'{nome}','{preco}',{quantidade})"

    inserir_dados = declaracao + dados

    try:
        con = mysql.connector.connect(host='localhost', database='teste', user='root', password='m123')
        cursor = con.cursor()
        cursor.execute(inserir_dados)
        con.commit()
        print(cursor.rowcount, "registros inseridos na tabela")
        cursor.close()
    except Error as e:
        print("Falha ao inserir dados no MySQL: {}".format(e))
    finally:
        if con.is_connected():
            con.close()
            print("Conexão com MySQL foi encerrada")

def deleta_dados(id):
    try:
        con = mysql.connector.connect(host='localhost', database='teste', user='root', password='m123')
        cursor = con.cursor()
        deleta_sql = f'delete from tbl_produtos where id={id}'
        cursor.execute(deleta_sql)
        con.commit()
        print(f'linha deletada com sucesso')
    except Error as e:
        print("Falha ao consultar tabela no MySQL:", e)
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()

def renova_dados(id):
    request_data = request.get_json()
    nome = None
    if request_data:
        if 'nome' in request_data:
            nome = request_data['nome']

        declaracao = f'UPDATE tbl_produtos SET nome="{nome}" where id={id}'
    try:
        con = mysql.connector.connect(host='localhost', database='teste', user='root', password='m123')
        altera_preco = declaracao
        cursor = con.cursor()
        cursor.execute(altera_preco)
        con.commit()
        print("Preco alterado com sucesso!")
    except Error as e:
        print("Falha ao inserir dado no MySQL:", e)
    finally:
        if (con.is_connected()):
            cursor.close()
            con.close()

consulta()
print(produtos)

#routes
@app.route('/', methods=['GET'])
def home():
    return jsonify("Este é o diretorio root da aplicacao")

@app.route('/api/v1/resources/produtos/all', methods=['GET'])
def api_all():
    consulta()

    return jsonify(produtos)

@app.route('/api/v1/resources/produtos/<int:id>', methods=['GET'])
def api_id(id):
    results = []
    for produto in produtos:
        if produto['Id'] == id:
            results.append(produto)

    return jsonify(results)

@app.route('/api/v1/resources/produtos/criar', methods=['POST'])
def criar():
    insere_dados()
    consulta()

    return jsonify(produtos)

@app.route('/api/v1/resources/produtos/<int:id>', methods=['DELETE'])
def deletar(id):
    deleta_dados(id)
    consulta()

    return jsonify(produtos)

@app.route('/api/v1/resources/produtos/<int:id>', methods=['PUT'])
def atualizar(id):
    renova_dados(id)
    consulta()
    return jsonify(produtos)

app.run()