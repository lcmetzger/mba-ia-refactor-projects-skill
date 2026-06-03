from flask import jsonify
from src.models.pedido_model import PedidoModel
from src.database.connection import db

# T-11: Extract magic numbers to constants
DISCOUNT_TIERS = [
    (10000, 0.10),
    (5000, 0.05),
    (1000, 0.02),
]

def calcular_desconto(faturamento):
    for threshold, rate in DISCOUNT_TIERS:
        if faturamento > threshold:
            return faturamento * rate
    return 0

def relatorio_vendas():
    try:
        stats = PedidoModel.get_stats()
        faturamento = stats["faturamento"]
        desconto = calcular_desconto(faturamento)

        return jsonify({
            "dados": {
                "total_pedidos": stats["total_pedidos"],
                "faturamento_bruto": round(faturamento, 2),
                "desconto_aplicavel": round(desconto, 2),
                "faturamento_liquido": round(faturamento - desconto, 2),
                "pedidos_status": stats["status_counts"],
                "ticket_medio": round(faturamento / stats["total_pedidos"], 2) if stats["total_pedidos"] > 0 else 0
            },
            "sucesso": True
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def health_check():
    # T-05 Mitigation: Sanitize health check output
    try:
        stats = PedidoModel.get_stats()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": produtos_count,
                "usuarios": usuarios_count,
                "pedidos": stats["total_pedidos"]
            },
            "versao": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500
