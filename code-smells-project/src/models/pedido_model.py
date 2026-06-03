from src.database.connection import db

class PedidoModel:
    @staticmethod
    def create(usuario_id, total, itens):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
                (usuario_id, total)
            )
            pedido_id = cursor.lastrowid

            for item in itens:
                cursor.execute(
                    "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                    (pedido_id, item["produto_id"], item["quantidade"], item["preco"])
                )
                
                cursor.execute(
                    "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                    (item["quantidade"], item["produto_id"])
                )

            conn.commit()
            return pedido_id
        except Exception as e:
            conn.rollback()
            raise e

    @staticmethod
    def get_by_usuario(usuario_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # AP-09 Mitigation: Use JOIN to fetch order items in a structured way
        # Since sqlite3 doesn't have JSON support in older versions, 
        # we'll fetch joined rows and group them in Python.
        query = """
            SELECT p.id, p.usuario_id, p.status, p.total, p.criado_em,
                   i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido i ON i.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = i.produto_id
            WHERE p.usuario_id = ?
        """
        cursor.execute(query, (usuario_id,))
        rows = cursor.fetchall()
        
        pedidos = {}
        for row in rows:
            pedido_id = row["id"]
            if pedido_id not in pedidos:
                pedidos[pedido_id] = {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": []
                }
            
            if row["produto_id"]:
                pedidos[pedido_id]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"],
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"]
                })
        
        return list(pedidos.values())

    @staticmethod
    def get_all():
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT p.id, p.usuario_id, p.status, p.total, p.criado_em,
                   i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido i ON i.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = i.produto_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        pedidos = {}
        for row in rows:
            pedido_id = row["id"]
            if pedido_id not in pedidos:
                pedidos[pedido_id] = {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": []
                }
            
            if row["produto_id"]:
                pedidos[pedido_id]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"],
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"]
                })
        
        return list(pedidos.values())

    @staticmethod
    def update_status(pedido_id, status):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedidos SET status = ? WHERE id = ?",
            (status, pedido_id)
        )
        conn.commit()
        return True

    @staticmethod
    def get_stats():
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total) FROM pedidos")
        faturamento = cursor.fetchone()[0] or 0

        cursor.execute("SELECT status, COUNT(*) FROM pedidos GROUP BY status")
        status_counts = dict(cursor.fetchall())

        return {
            "total_pedidos": total_pedidos,
            "faturamento": faturamento,
            "status_counts": status_counts
        }
