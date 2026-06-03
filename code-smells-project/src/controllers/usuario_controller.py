from flask import request, jsonify
from src.models.usuario_model import UsuarioModel

def listar():
    try:
        usuarios = UsuarioModel.get_all()
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def buscar(id):
    try:
        usuario = UsuarioModel.get_by_id(id)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True}), 200
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def criar():
    try:
        dados = request.get_json()
        if not dados or not all(k in dados for k in ("nome", "email", "senha")):
            return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

        id = UsuarioModel.create(dados["nome"], dados["email"], dados["senha"])
        return jsonify({"dados": {"id": id}, "sucesso": True}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def login():
    try:
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400

        usuario = UsuarioModel.login(email, senha)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
        else:
            return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
