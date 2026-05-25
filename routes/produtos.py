from flask import Blueprint, jsonify, request
from contextlib import contextmanager
from db import conectar

produtos_bp = Blueprint('produtos', __name__)

# ---------------------------------------------------------------------------
# Helper de conexão — elimina duplicação em todos os endpoints
# ---------------------------------------------------------------------------

@contextmanager
def get_cursor(dictionary=False):
    
    con = conectar()
    if not con:
        raise ConnectionError('Erro ao conectar ao banco de dados.')
    cursor = con.cursor(dictionary=dictionary)
    try:
        yield cursor, con
    finally:
        cursor.close()
        con.close()


def validar_numero_positivo(valor, nome_campo):
    
    if not isinstance(valor, (int, float)) or valor < 0:
        return f"'{nome_campo}' deve ser um número positivo."
    return None


# ---------------------------------------------------------------------------
# GET /produtos  — listar todos
# ---------------------------------------------------------------------------

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        with get_cursor(dictionary=True) as (cursor, _):
            cursor.execute('''
                SELECT id, nome, marca, estoque, categoria_id, preco
                FROM produtos
            ''')
            produtos = cursor.fetchall()
        return jsonify(produtos), 200

    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao listar produtos.', 'detalhe': str(e)}), 500


# ---------------------------------------------------------------------------
# GET /produtos/<id>  — buscar por ID
# ---------------------------------------------------------------------------

@produtos_bp.route('/produtos/<int:id>', methods=['GET'])
def obter_produto_por_id(id):
    try:
        with get_cursor(dictionary=True) as (cursor, _):
            cursor.execute('''
                SELECT id, nome, marca, estoque, categoria_id, preco
                FROM produtos
                WHERE id = %s
            ''', (id,))
            produto = cursor.fetchone()

        if not produto:
            return jsonify({'error': 'Produto não encontrado.'}), 404

        return jsonify(produto), 200

    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar produto.', 'detalhe': str(e)}), 500


# ---------------------------------------------------------------------------
# POST /produtos  — criar produto
# ---------------------------------------------------------------------------

@produtos_bp.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()

    campos_obrigatorios = ['nome', 'marca', 'preco', 'estoque', 'categoria_id']
    if not data or not all(c in data for c in campos_obrigatorios):
        return jsonify({'error': 'Campos obrigatórios faltando.', 'obrigatorios': campos_obrigatorios}), 400


    for campo in ('preco', 'estoque'):
        erro = validar_numero_positivo(data[campo], campo)
        if erro:
            return jsonify({'error': erro}), 400

    try:
        with get_cursor(dictionary=True) as (cursor, con):
            
            cursor.execute('SELECT id FROM categoria WHERE id = %s', (data['categoria_id'],))
            if not cursor.fetchone():
                return jsonify({'error': 'Categoria não encontrada.'}), 404

            cursor.execute('''
                INSERT INTO produtos (nome, marca, preco, estoque, categoria_id)
                VALUES (%s, %s, %s, %s, %s)
            ''', (data['nome'], data['marca'], data['preco'], data['estoque'], data['categoria_id']))

            novo_id = cursor.lastrowid
            con.commit()


            cursor.execute('''
                SELECT id, nome, marca, estoque, categoria_id, preco
                FROM produtos WHERE id = %s
            ''', (novo_id,))
            produto = cursor.fetchone()

        return jsonify({'mensagem': 'Produto criado com sucesso!', 'produto': produto}), 201

    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao criar produto.', 'detalhe': str(e)}), 500


# ---------------------------------------------------------------------------
# PUT /produtos/<id>  — atualizar produto
# ---------------------------------------------------------------------------

@produtos_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado enviado.'}), 400

    
    for campo in ('preco', 'estoque'):
        if campo in data:
            erro = validar_numero_positivo(data[campo], campo)
            if erro:
                return jsonify({'error': erro}), 400

    try:
        with get_cursor(dictionary=True) as (cursor, con):

            cursor.execute('SELECT id, nome, marca, preco, estoque, categoria_id FROM produtos WHERE id = %s', (id,))
            produto = cursor.fetchone()
            if not produto:
                return jsonify({'error': 'Produto não encontrado.'}), 404

            if 'categoria_id' in data:
                cursor.execute('SELECT id FROM categoria WHERE id = %s', (data['categoria_id'],))
                if not cursor.fetchone():
                    return jsonify({'error': 'Categoria não encontrada.'}), 404


            atualizado = {
                'nome':         data.get('nome',         produto['nome']),
                'marca':        data.get('marca',        produto['marca']),
                'preco':        data.get('preco',        produto['preco']),
                'estoque':      data.get('estoque',      produto['estoque']),
                'categoria_id': data.get('categoria_id', produto['categoria_id']),
            }

            cursor.execute('''
                UPDATE produtos
                SET nome = %s, marca = %s, preco = %s, estoque = %s, categoria_id = %s
                WHERE id = %s
            ''', (
                atualizado['nome'],
                atualizado['marca'],
                atualizado['preco'],
                atualizado['estoque'],
                atualizado['categoria_id'],
                id,
            ))
            con.commit()


            cursor.execute('''
                SELECT id, nome, marca, estoque, categoria_id, preco
                FROM produtos WHERE id = %s
            ''', (id,))
            produto_atualizado = cursor.fetchone()

        return jsonify({'mensagem': 'Produto atualizado com sucesso!', 'produto': produto_atualizado}), 200

    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar produto.', 'detalhe': str(e)}), 500


# ---------------------------------------------------------------------------
# DELETE /produtos/<id>  — deletar produto
# ---------------------------------------------------------------------------

@produtos_bp.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    try:
        with get_cursor(dictionary=True) as (cursor, con):
            cursor.execute('SELECT id, nome FROM produtos WHERE id = %s', (id,))
            produto = cursor.fetchone()
            if not produto:
                return jsonify({'error': 'Produto não encontrado.'}), 404

            cursor.execute('DELETE FROM produtos WHERE id = %s', (id,))
            
            con.commit()

        return jsonify({'mensagem': f"Produto '{produto['nome']}' deletado com sucesso!"}), 200

    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar produto.', 'detalhe': str(e)}), 500