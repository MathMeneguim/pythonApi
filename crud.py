import mysql.connector
from mysql.connector import Error
#tirar conteudo anterior ao try das funcoes e colocar dentro das estruturas condicionais
def conectar():
    try:
        global con
        con = mysql.connector.connect(host='localhost', database='teste',user='root', password='m123')
    except Error as e:
        print("Erro na conexão com MySQL",e)

def consulta():
    try:
        conectar()
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute("select database();")
            cursor.fetchone()
            consulta = "select * from tbl_produtos;"
            cursor.execute(consulta)
            linhas = cursor.fetchall()

            print("\nMostrando produtos cadastrados:")
            for i in linhas:
                print("Id:", i[0])
                print("Nome:", i[1])
                print("Preco:", i[2])
                print("Quantidade:", i[3], "\n")
    except Error as e:
        print("Erro ao acessar a tabela MySQL", e, "\n")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexao com MySQL foi encerrada")

def consulta_id(id):
    try:
        conectar()
        consulta_sql = 'select * from tbl_produtos where id={}'.format(id)
        cursor = con.cursor()
        cursor.execute(consulta_sql)
        linhas = cursor.fetchall()
        for linha in linhas:
            print("id:",linha[0])
            print("Produto:",linha[1])
            print("Preco:", linha[2])
        cursor.close()
    except Error as e:
        print("Falha ao consultar tabela no MySQL:", e)
    finally:
        if(con.is_connected()):
            con.close()

def insere_dados(inserir_dados):
    try:
        conectar()
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

def atualiza(declaracao):
    try:
        conectar()
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

def deleta(id):
    try:
        conectar()
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

print("Digite qual funcao deseja executa no MySQL:\n"
      "0-consulta | 1-consulta_id | 2-insere_dados | 3-atualiza | 4-deleta")

acao = int(input("Funcao:"))

if acao == 0:
    consulta()

if acao == 1:
    id = int(input('digite o id para consulta:'))
    consulta_id(id)

if acao == 2:
    print("Entre com os dados conforme solicitado:")

    nome = input("Nome do produto:")
    preco = input("Digite o preco do produto:")
    quantidade = input("Digite a quantidade do produto:")
    declaracao = '''INSERT INTO tbl_produtos(nome,preco,quantidade)
        VALUES ('''
    dados = f"'{nome}','{preco}',{quantidade})"

    inserir_dados = declaracao + dados
    insere_dados(inserir_dados)

if acao == 3:
    print("Digite o codigo do produto a ser alterado:")
    id = input("Id do produto:")
    consulta_id(id)
    print("\nEntre com o novo preço do produto")
    preco = input("Preço:")
    declaracao = """UPDATE tbl_produtos
           SET preco=""" + preco + """
           WHERE id=""" + id

    print(declaracao)
    atualiza(declaracao)

if acao == 4:
    print("Digite o codigo do produto a ser deletado:")
    id = input("Id do produto:")
    deleta(id)