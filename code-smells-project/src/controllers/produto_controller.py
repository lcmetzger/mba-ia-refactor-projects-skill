from flask import request, jsonify
from src.models.produto_model import ProdutoModel

def listar():
    try:
        produtos = ProdutoModel.get_all()
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def buscar(id):
    try:
        produto = ProdutoModel.get_by_id(id)
        if produto:
            return jsonify({"dados": produto, "sucesso": True}), 200
        else:
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def criar():
    try:
        dados = request.get_json()

        if not dados or "nome" not in dados or "preco" not in dados or "estoque" not in dados:
            return jsonify({"erro": "Dados obrigatórios ausentes"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0 or estoque < 0 or len(nome) < 2 or len(nome) > 200:
            return jsonify({"erro": "Validação de campos falhou"}), 400

        categorias_validas = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
        if categoria not in categorias_validas:
            return jsonify({"erro": "Categoria inválida"}), 400

        id = ProdutoModel.create(nome, descricao, preco, estoque, categoria)
        return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def atualizar(id):
    try:
        dados = request.get_json()
        produto_existente = ProdutoModel.get_by_id(id)
        if not produto_existente:
            return jsonify({"erro": "Produto não encontrado"}), 404

        if not dados or "nome" not in dados or "preco" not in dados or "estoque" not in dados:
            return jsonify({"erro": "Dados obrigatórios ausentes"}), 400

        ProdutoModel.update(id, dados["nome"], dados.get("descricao", ""), 
                             dados["preco"], dados["estoque"], dados.get("categoria", "geral"))
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def deletar(id):
    try:
        if not ProdutoModel.get_by_id(id):
            return jsonify({"erro": "Produto não encontrado"}), 404
        ProdutoModel.delete(id)
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def buscar_avancado():
    try:
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria")
        preco_min = request.args.get("preco_min")
        preco_max = request.args.get("preco_max")

        if preco_min: preco_min = float(preco_min)
        if preco_max: preco_max = float(preco_max)

        resultados = ProdutoModel.search(termo, categoria, preco_min, preco_max)
        return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
