# -*- coding: utf-8 -*-
"""requests.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m0prubu5KO6Mhw44Vx0HftziNurIAuv5
"""
import requests

# Pegar info - GET
requisicao = requests.get("https://projeto-teste-66f06-default-rtdb.firebaseio.com/.json")
print(requisicao)
print(requisicao.json())

# Criar info - POST  --> precisamos sempre passar informacoes junto
informacoes = '{"nome":"Marina"}'
requisicao = requests.post("https://projeto-teste-66f06-default-rtdb.firebaseio.com/.json", data=informacoes)
print(requisicao)
print(requisicao.json())

# Atualizar info - PATCH --> precisamos sempre passar informacoes junto tbm
informacoes = '{"nome":"giovanna", "sobrenome":"cucato","idade":"20"}'
requisicao = requests.patch("/-N6mcthkZGok69Pd5QMy.json", data=informacoes)
print(requisicao)
print(requisicao.json())

# Deletar info - DELETE
requisicao = requests.delete("https://projeto-teste-66f06-default-rtdb.firebaseio.com/-N6mfudp8mx215LBoZpd.json", data=informacoes)
print(requisicao)
print(requisicao.json())