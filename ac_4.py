#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Código para gerar boletos a partir do banco Santander

import sys
import pyboleto
from pyboleto.bank.santander import BoletoSantander
from pyboleto.html import BoletoHTML
import datetime
from pyboleto.pdf import BoletoPDF
from flask import Flask, request, render_template
from contextlib import closing
import sqlite3
from django.shortcuts import render
import os
import webbrowser

app = Flask(__name__)

boleto_PDF = ''

if sys.version_info < (3,):
    from pyboleto.pdf import BoletoPDF
    
nome = ''    
documento = ''
valor = ''
    
@app.route("/")
def menu():
    return render_template("gerarboleto.html", mensagem = "")

@app.route("/gerarboleto", methods = ["GET"])
def form_gerar_boleto_api():
    return render_template("gerarboleto.html")

@app.route("/gerarboleto", methods = ["POST"])
def gerar_boleto_api():
    nome = request.form["nome"]
    documento = request.form["documento"]
    valor = request.form["valor"]
    get_data_santander(nome,documento,valor)
    print_all(nome,documento,valor)
    webbrowser.open(os.getcwd() + '/templates/boleto-' + 'santander' + '-' + documento +'.html')    
    return render_template('gerarboleto.html',mensagem ='Gerado!') 

def get_data_santander(nome,documento,valor):
    listaDados = []
    for i in range(2):
        d = BoletoSantander()
        d.agencia_cedente = '1333'
        d.conta_cedente = '070707'
        d.data_vencimento = datetime.date.today()
        d.data_documento = datetime.date.today()
        d.data_processamento = datetime.date.today()
        d.valor_documento = valor
        d.nosso_numero = '1234567'
        d.numero_documento = '12345'
        d.ios = '0'
        cliente = nome + ' - ' + documento
        d.cedente = 'Marmifit Marmitas Deliciosas LTDA'
        d.cedente_documento = "912.082.084-18"
        d.cedente_endereco = "Rua Rudge, 500 - Centro - Sao Paulo/SP - \
        CEP: 12345-678"

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
            ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
            ]
        d.valor_documento = valor

        d.sacado = [
            cliente,
            "Rua Logradouro, 00 - Bairro - Cidade - UF - Cep. 00000-000",
            ""
            ]
        listaDados.append(d)
        
    return listaDados


def print_all(nome,documento,valor):
    banks = {
        #"itau": "Itau",
        #"bb": "Banco do Brasil",
        #"caixa": "Caixa",
        #"real": "Real",
        "santander": "Santander",
        #"bradesco": "Bradesco",
    }
    for bank in banks:
        print("Gerando boleto para o banco " + banks[bank])
        data_func_name = "get_data_" + bank
        data_func = eval(data_func_name)
        boleto_datas = data_func(nome,documento,valor)
        if sys.version_info < (3,):
            boleto_PDF = BoletoPDF('boleto-' + bank + '-normal-teste.pdf')
        boleto_HTML = BoletoHTML('templates/boleto-' + 'santander' + '-' + documento +'.html')
        for boleto_data in boleto_datas:
            if sys.version_info < (3,):
                boleto_PDF.drawBoleto(boleto_data)
                boleto_PDF.nextPage()
                boleto_PDF.save()
            boleto_HTML.drawBoleto(boleto_data)
            boleto_HTML.nextPage()
            boleto_HTML.save()



if __name__ == "__main__":
    #print_all()
    app.run()
    
