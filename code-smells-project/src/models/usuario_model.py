from src.database.connection import db

class UsuarioModel:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        cursor = conn.cursor()
        # AP-06 Mitigation: Exclude 'senha' from results
        cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(usuario_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        # AP-06 Mitigation: Exclude 'senha' from results
        cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def create(nome, email, senha, tipo="cliente"):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo)
        )
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def login(email, senha):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, email, tipo FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
