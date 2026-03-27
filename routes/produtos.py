from flask import Blueprint, jsonify, request
from db import conectar
from collections import OrderedDict

produtos_bp = Blueprint('produtos', __name__)

# Método GET para listar os produtos 
@produtos_bp.route('/produtos', methods=['GET']) 
def listar_produtos(): 
    con = conectar() 
    if not con: 
        return jsonify({'Error': 'Erro ao efetuar conexão com o banco de dados.'}), 500 
    
    cursor = con.cursor(dictionary=True) 

    try:    
        cursor.execute('''
                SELECT id, nome, marca, cstoque, categoria_ID, preco
                FROM produtos
            ''')

        produtos = cursor.fetchall() 

    except Exception as e:
        return jsonify({'Error': str(e)}), 500

    finally:
        cursor.close()
        con.close()

    return jsonify(produtos)

@produtos_bp.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()

    if not data or not all(i in data for i in ['nome', 'marca', 'preco', 'estoque', 'categoria_id']):
        return jsonify({
            'Error': 'Campos obrigatórios faltando.'
        }), 400

    con = conectar()
    cursor = con.cursor()

    try:
        cursor.execute('SELECT * FROM Categoria WHERE ID = %s', (data['categoria_id'],))
        
        if not cursor.fetchone():
            return jsonify({'Error': 'Categoria não encontrada.'}), 404

        sql = '''
            INSERT INTO produtos (Nome, Marca, Preco, Estoque, Categoria_ID)
            VALUES (%s, %s, %s, %s, %s)
        '''

        valores = (
            data['nome'],
            data['marca'],
            data['preco'],
            data['estoque'],
            data['categoria_id']
        )

        cursor.execute(sql, valores)
        con.commit()

        return jsonify({
            'Mensagem': 'Produto criado!',
            'id': cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({
            'Error': 'Erro ao criar o produto.',
            'Detalhe': str(e)
        }), 500

    finally:
        cursor.close()
        con.close()