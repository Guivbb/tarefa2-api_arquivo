from flask import Flask, request, jsonify
import pandas as pd

app=Flask(__name__)
arquivo="arquivo.csv"

@app.route('/')
def index():
    return "API está funcionando"

@app.route('/csv',methods=['POST'])
def criaArquivo():
    dados= request.get_json()
    if not isinstance(dados,list) or len(dados)==0:
        return jsonify({"erro":"lista de objetos do corpo de requisição vazia"}), 400
    try:
        data_frame=pd.DataFrame(dados)
        data_frame.to_csv(arquivo,index=False,encoding='utf-8')
        return jsonify({"mensagem":"arquivo criado com sucesso"})
    except Exception as e:
        return jsonify({"erro":f"erro ao criar o arquivo CSV: {str(e)}"}), 500

@app.route('/csv',methods=['PATCH'])
def adicionaLinha():
    novos_dados=request.get_json()
    if not isinstance(novos_dados,list) or len(novos_dados)==0:
        return jsonify({"erro":"lista de objetos do corpo de requisição vazia"}), 400
    try:
        pd.read_csv(arquivo)
        data_frame_novo=pd.DataFrame(novos_dados)
        data_frame_novo.to_csv(arquivo,mode='a',header=False,index=False,encoding='8')
        return jsonify({"mensagem":"nova linha criada com sucesso"}),200
    except FileExistsError:
        return jsonify({"erro":"arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro":f"erro ao adicionar novas linhas{str(e)}"}), 500

@app.route('/csv/linha/ind_linha',methods=['DELETE'])
def deletaLinha(ind_linha):
    try:
        data_frame=pd.read_csv(arquivo)
        if ind_linha<0 or ind_linha>=len(data_frame):
            return jsonify({"erro":f"indice fora do intervalo de 0 a {len(data_frame)-1}"}), 400
        data_frame=data_frame.drop(data_frame.index[ind_linha])
        data_frame.to_csv(arquivo,index=False,encoding='8'),400
        return jsonify({"mensagem":f"linha {ind_linha} removida com sucesso"})
    except FileExistsError:
        return jsonify({"erro":"arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"ocorreu um erro ao deletar a linha: {str(e)}"}), 500
    
@app.route('/csv',methods=['GET'])
def leArquivo():
    try:
        data_frame=pd.read_csv(arquivo)
        inicio=request.args.get('inicio',default=None,type=int)
        final=request.args.get('final',default=None,type=int)
        if inicio is not None and final is not None:
            data_frame=data_frame.iloc[inicio:final]
        resultado=data_frame.to_dict(orient='records')
        return jsonify(resultado), 200
    except FileExistsError:
        return jsonify({"erro":"arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"ocorreu um erro ao ler o arquivo: {str(e)}"}), 500
    
@app.route('/csv/filtrar', methods=['GET'])
def filtrar_csv():
    nome_coluna= request.args.get('coluna')
    valor= request.args.get('valor_menor', type=float)
    if not nome_coluna or valor is None:
        return jsonify({"erro":"os parâmetros 'coluna' e 'valor_menor' são obrigatórios"}), 400
    try:
        data_frame=pd.read_csv(arquivo)
        if nome_coluna not in data_frame.columns:
            return jsonify({"erro":f"a coluna {nome_coluna} "})
        data_frame_filtrado=data_frame[data_frame[nome_coluna]<valor]
        resultado=data_frame_filtrado.to_dict(orient='records')
        return jsonify(resultado), 200
    except FileExistsError:
        return jsonify({"erro":"arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"ocorreu um erro ao filtrar dados: {str(e)}"}), 500

@app.route('/csv/genero',methods=['GET'])
def buscaporGenero():
    nomedoGenero=request.args.get('nome')
    ordenar=request.args.get('ordenar',default='Rating')
    ordem=request.args.get('ordem', default='desc').lower()
    if not nomedoGenero:
        return jsonify({"erro": "O parâmetro 'nome' do gênero é obrigatório."}), 400
    if ordem not in ['asc', 'desc']:
        return jsonify({"erro": "O parâmetro 'ordem' deve ser 'cres' ou 'desc'."}), 400
    try:
        data_frame=pd.read_csv(arquivo)
        data_frame_filtrado=data_frame[data_frame['Gênero'].str.lower()==nomedoGenero.lower()]
        if data_frame_filtrado.empty:
            return jsonify({"mensagem": f"Nenhum filme encontrado para o gênero '{nomedoGenero}'."}), 404
        if ordenar not in data_frame_filtrado.columns:
            return jsonify({"erro": f"Coluna para ordenação ('{ordenar}') não existe."}), 400  
        crescente = True if ordem == 'asc' else False
        data_frame_ordenado = data_frame_filtrado.sort_values(by=ordenar, ascending=crescente)
        resultado = data_frame_ordenado.to_dict(orient='records')
        return jsonify(resultado), 200
    except FileNotFoundError:
        return jsonify({"erro": "arquivo não encontrado."}), 404
    except Exception as e:
        return jsonify({"erro": f"ocorreu um erro: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)


