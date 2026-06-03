from flask import request, jsonify
from src.models.pedido_model import PedidoModel
from src.models.produto_model import ProdutoModel
from src.services.notification_service import notify_order_created, notify_order_status_update

def criar():
    try:
        dados = request.get_json()
        if not dados: return jsonify({"erro": "Dados inválidos"}), 400

        usuario_id = dados.get("usuario_id")
        itens_req = dados.get("itens", [])

        if not usuario_id or not itens_req:
            return jsonify({"erro": "Usuario ID e itens são obrigatórios"}), 400

        total = 0
        itens_validados = []
        for item in itens_req:
            produto = ProdutoModel.get_by_id(item["produto_id"])
            if not produto:
                return jsonify({"erro": f"Produto {item['produto_id']} não encontrado"}), 400
            if produto["estoque"] < item["quantidade"]:
                return jsonify({"erro": f"Estoque insuficiente para {produto['nome']}"}), 400
            
            total += produto["preco"] * item["quantidade"]
            itens_validados.append({
                "produto_id": item["produto_id"],
                "quantidade": item["quantidade"],
                "preco": produto["preco"]
            })

        pedido_id = PedidoModel.create(usuario_id, total, itens_validados)
        notify_order_created(pedido_id, usuario_id)

        return jsonify({
            "dados": {"pedido_id": pedido_id, "total": total},
            "sucesso": True,
            "mensagem": "Pedido criado com sucesso"
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def listar_usuario(usuario_id):
    try:
        pedidos = PedidoModel.get_by_usuario(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def listar_todos():
    try:
        pedidos = PedidoModel.get_all()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def atualizar_status(pedido_id):
    try:
        dados = request.get_json()
        novo_status = dados.get("status")
        valid_statuses = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
        
        if novo_status not in valid_statuses:
            return jsonify({"erro": "Status inválido"}), 400

        PedidoModel.update_status(pedido_id, novo_status)
        notify_order_status_update(pedido_id, novo_status)

        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
