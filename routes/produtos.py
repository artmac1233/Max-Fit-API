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
                SELECT id, nome, marca, estoque, categoria_ID, preco
                FROM produtos
            ''')

        produtos = cursor.fetchall() 

    except Exception as e:
        return jsonify({'Error': str(e)}), 500

    finally:
        cursor.close()
        con.close()

    return jsonify(produtos)

#Método POST para criação de um novo produto

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

#Método PUT para atualizar um protudo

@produtos_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):

    data = request.get_json()

    if not data:
        return jsonify({
            'Error': 'Nenhum dado enviado.'
        }), 400

    con = conectar()

    if not con:
        return jsonify({
            'Error': 'Erro ao conectar ao banco.'
        }), 500

    cursor = con.cursor(dictionary=True)

    try:

        cursor.execute(
            'SELECT * FROM produtos WHERE ID = %s',
            (id,)
        )

        produto = cursor.fetchone()

        if not produto:
            return jsonify({
                'Error': 'Produto não encontrado.'
            }), 404

        if 'categoria_id' in data:

            cursor.execute(
                'SELECT 1 FROM Categoria WHERE ID = %s',
                (data['categoria_id'],)
            )

            if not cursor.fetchone():
                return jsonify({
                    'Error': 'Categoria não encontrada.'
                }), 404

        produto_atualizado = {
            'nome': data.get('nome', produto['Nome']),
            'marca': data.get('marca', produto['Marca']),
            'preco': data.get('preco', produto['Preco']),
            'estoque': data.get('estoque', produto['Estoque']),
            'categoria_id': data.get('categoria_id', produto['Categoria_ID'])
        }

        sql = '''
            UPDATE produtos
            SET
                Nome = %s,
                Marca = %s,
                Preco = %s,
                Estoque = %s,
                Categoria_ID = %s
            WHERE ID = %s
        '''

        cursor.execute(sql, (
            produto_atualizado['nome'],
            produto_atualizado['marca'],
            produto_atualizado['preco'],
            produto_atualizado['estoque'],
            produto_atualizado['categoria_id'],
            id
        ))

        con.commit()

        return jsonify({
            'Mensagem': 'Produto atualizado com sucesso!'
        }), 200

    except Exception as e:

        return jsonify({
            'Error': 'Erro ao atualizar produto.',
            'Detalhe': str(e)
        }), 500

    finally:
        cursor.close()
        con.close()

#Método DELETE para deletar um produto

@produtos_bp.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produtos(id):

    con=conectar()
    
    if not con:
        return jsonify({
            'Error': 'Erro ao conectar ao banco.'
        }), 500
    
    cursor=con.cursor(dictionary=True)
    
    try:
        cursor.execute(
            'SELECT * FROM produtos WHERE ID = %s',
            (id,)
        ) 

        produto=cursor.fetchone()

        if not produto:
            return jsonify({
                'Error':'Produto inexistente',
            }), 404

        cursor.execute(
            'DELETE FROM produtos WHERE ID = %s',
            (id,)
        ) 

        produto = cursor.fetchone()

        con.commit()

        return jsonify({
            'Mensagem': 'Produto deletado com sucesso!'
        }), 200

    except Exception as e:
        return jsonify({
            'Error': 'Erro ao deletar o produto.',
            'Detalhe': str(e)
        }), 500
    
    finally:
        cursor.close()
        con.close()