from src.database.connection import db

class ProdutoModel:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(produto_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def create(nome, descricao, preco, estoque, categoria):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            (nome, descricao, preco, estoque, categoria)
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(produto_id, nome, descricao, preco, estoque, categoria):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
            (nome, descricao, preco, estoque, categoria, produto_id)
        )
        conn.commit()
        return True

    @staticmethod
    def delete(produto_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        return True

    @staticmethod
    def search(termo, categoria=None, preco_min=None, preco_max=None):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        
        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{termo}%", f"%{termo}%"])
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max:
            query += " AND preco <= ?"
            params.append(preco_max)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
