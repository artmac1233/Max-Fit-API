from flask import Blueprint, jsonify, request
from contextlib import contextmanager
from db import conectar
import bcrypt
import re

clientes_bp = Blueprint('clientes', __name__)

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

def validar_senha(senha):

    if len(senha) < 8:
        return 'A senha deve ter pelo menos 8 caracteres.'

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(padrao, email):
        return 'Email inválido.'

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        with get_cursor(dictionary=True) as (cursor, _):
            cursor.execute('''
                SELECT id, nome, email, telefone 
                FROM clientes
            ''')

            clientes = cursor.fetchall()
        return jsonify(clientes), 200
    
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error':'Erro ao listar os clientes.', 'detalhe':str(e)}), 500
    
@clientes_bp.route('/clientes/<int:id>', methods=['GET'])
def listar_clientes_por_id(id):
    try:
        with get_cursor(dictionary=True) as (cursor, _):
            cursor.execute('''
                SELECT id, nome, email, telefone 
                FROM clientes
                WHERE id = %s
            ''', (id,))

            cliente = cursor.fetchone()

            if not cliente:
                return jsonify({'error': 'Cliente não encontrado.'}), 404
        
        return jsonify(cliente), 200
    
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar cliente.', 'detalhe': str(e)}), 500
    
@clientes_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()

    campos_obrigatorios = ['nome','email','senha','telefone']
    if not data or not all(c in data for c in campos_obrigatorios):
        return jsonify({'error': 'Campos obrigatórios faltando.', 'obrigatorios': campos_obrigatorios}), 400
    
    erro = validar_email(data['email'])
    if erro:
        return jsonify({'error': erro}), 400

    erro = validar_senha(data['senha'])
    if erro:
        return jsonify({'error': erro}), 400
        
    try:
        with get_cursor(dictionary=True) as (cursor, con):

            senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())

            cursor.execute('''
                INSERT INTO clientes (nome, email, telefone, senha)
                VALUES  (%s,%s,%s,%s)
            ''', (data['nome'], data['email'], data['telefone'], senha_hash))

            novo_id = cursor.lastrowid
            con.commit()
            
            cursor.execute('''
                SELECT id, nome, email
                FROM clientes 
                WHERE id = %s   
            ''', (novo_id,))
            cliente = cursor.fetchone()

        return jsonify({'mensagem':'Usuario criado com sucesso!', 'cliente': cliente}), 201

    except ConnectionError as e:
        return jsonify({'erro': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao criar cliente.', 'detalhe': str(e)}), 500

@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    data = request.get_json()

    if not data:
        return jsonify({'erro':'Nenhum dado enviado.'}), 400

    if 'email' in data:
        erro_email = validar_email(data['email'])
        if erro_email:
            return jsonify({'error': erro_email}), 400
        
        if 'senha_atual' not in data:
            return jsonify({'error': 'Confirme sua senha para alterar o email.'}), 400

    if 'senha' in data:
        erro_senha = validar_senha(data['senha'])
        if erro_senha:
            return jsonify({'error': erro_senha}), 400
        
        if 'senha_atual' not in data:
            return jsonify({'error': 'Confirme sua senha atual.'}), 400
        
        if 'confirmar_senha' not in data:
            return jsonify({'error': 'Confirmação de senha obrigatória.'}), 400
    
        if data['senha'] != data['confirmar_senha']:
            return jsonify({'error': 'As senhas não coincidem.'}), 400
    
    try:
        with get_cursor(dictionary=True) as (cursor, con):
            cursor.execute('SELECT id, nome, telefone, email, senha FROM clientes WHERE id = %s', (id,))
            cliente = cursor.fetchone()

            if not cliente:
                return jsonify({'error': 'Cliente não encontrado.'}), 404
            
            if 'email' in data:
                senha_banco = cliente['senha']
                if isinstance(senha_banco, str):
                    senha_banco = senha_banco.encode('utf-8')
    
                if not bcrypt.checkpw(data['senha_atual'].encode('utf-8'), senha_banco):
                    return jsonify({'error': 'Senha incorreta.'}), 401
                
            atualizado = {
                'nome':     data.get('nome',     cliente['nome']),
                'email':    data.get('email',    cliente['email']),
                'telefone': data.get('telefone', cliente['telefone']),
            }

            if 'senha' in data:
                senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
                cursor.execute('''
                    UPDATE clientes SET nome=%s, email=%s, telefone=%s, senha=%s WHERE id=%s
                ''', (atualizado['nome'], atualizado['email'], atualizado['telefone'], senha_hash, id))
            else:
                cursor.execute('''
                    UPDATE clientes SET nome=%s, email=%s, telefone=%s WHERE id=%s
                ''', (atualizado['nome'], atualizado['email'], atualizado['telefone'], id))
            
            con.commit()

            cursor.execute('''
                SELECT nome, email, telefone FROM clientes WHERE id = %s
            ''', (id,))
            cliente_atualizado = cursor.fetchone()

        return jsonify({'mensagem':'Cliente atualizado com sucesso!', 'cliente': cliente_atualizado}), 200

    except ConnectionError as e:
        return jsonify({'erro': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar cliente.', 'detalhe': str(e)}), 500

@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):

    try:
        with get_cursor(dictionary=True) as (cursor, con):

            cursor.execute('''
                SELECT id, nome, email
                FROM clientes
                WHERE id = %s
            ''', (id,))
            cliente = cursor.fetchone()
            if not cliente:
                return jsonify({'erro':'Cliente não encontrado'}), 404

            cursor.execute('''
                DELETE FROM clientes 
                WHERE id = %s
            ''', (id,))
            con.commit()

        return jsonify({'mensagem':f"Cliente '{cliente['nome']}' excluido com sucesso!"}), 200
    
    except ConnectionError as e:
        return jsonify({'erro': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao excluir cliente.', 'detalhe': str(e)}), 500
