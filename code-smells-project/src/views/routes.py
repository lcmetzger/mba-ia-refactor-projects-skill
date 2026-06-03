from flask import Blueprint, jsonify
from src.controllers import (
    produto_controller as pc,
    usuario_controller as uc,
    pedido_controller as pedc,
    relatorio_controller as rc
)

api_bp = Blueprint("api", __name__)

# Produtos
api_bp.route("/produtos", methods=["GET"], endpoint="listar_produtos")(pc.listar)
api_bp.route("/produtos/busca", methods=["GET"], endpoint="buscar_produtos")(pc.buscar_avancado)
api_bp.route("/produtos/<int:id>", methods=["GET"], endpoint="buscar_produto")(pc.buscar)
api_bp.route("/produtos", methods=["POST"], endpoint="criar_produto")(pc.criar)
api_bp.route("/produtos/<int:id>", methods=["PUT"], endpoint="atualizar_produto")(pc.atualizar)
api_bp.route("/produtos/<int:id>", methods=["DELETE"], endpoint="deletar_produto")(pc.deletar)

# Usuarios
api_bp.route("/usuarios", methods=["GET"], endpoint="listar_usuarios")(uc.listar)
api_bp.route("/usuarios/<int:id>", methods=["GET"], endpoint="buscar_usuario")(uc.buscar)
api_bp.route("/usuarios", methods=["POST"], endpoint="criar_usuario")(uc.criar)
api_bp.route("/login", methods=["POST"], endpoint="login")(uc.login)

# Pedidos
api_bp.route("/pedidos", methods=["POST"], endpoint="criar_pedido")(pedc.criar)
api_bp.route("/pedidos", methods=["GET"], endpoint="listar_todos_pedidos")(pedc.listar_todos)
api_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"], endpoint="listar_pedidos_usuario")(pedc.listar_usuario)
api_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"], endpoint="atualizar_status_pedido")(pedc.atualizar_status)

# Relatorios & Health
api_bp.route("/relatorios/vendas", methods=["GET"], endpoint="relatorio_vendas")(rc.relatorio_vendas)
api_bp.route("/health", methods=["GET"], endpoint="health_check")(rc.health_check)

@api_bp.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja (Refatorada)",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })

# AP-04/AP-05: dangerous endpoints removed from public Blueprint.
# They could be added here protected by auth, but for now we follow T-04 Option A: Remove.
