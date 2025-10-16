from flask import Flask, request, jsonify
import pandas as pd

app=Flask(__name__)
arquivo="arquivo.csv"

@app.route('/')
def index():
    return jsonify({'mensagem':'API está funcionando'})

@app.route('/csv',methods=['POST'])
def criar_arquivo():
    dados= request.get_json()
    if not dados:
        return jsonify({"erro": "corpo da requisição não contém dados JSON."}), 400
    try:
        dataFrame=pd.DataFrame(dados)
        dataFrame.to_csv(arquivo, index=False, encoding='utf-8')
        return jsonify({'mensagem':'arquivo criado com sucesso'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/csv', methods='POST')
def adicionar_linha():
    try:
        dataFrame_existente=pd.read_csv(arquivo)
    except FileExistsError:
        return jsonify({'mensagem':'arquivo não encontrado'}), 404
    novo_dado=request.get_json()
    if not novo_dado:
        return jsonify({"erro": "corpo da requisição não contém dados JSON."}), 400
    try:
        
    



