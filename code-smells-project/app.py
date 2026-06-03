from flask import Flask, jsonify
from flask_cors import CORS
from src.config.settings import config
from src.views.routes import api_bp
from src.database.connection import db

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app)
    
    # Register Blueprints
    app.register_blueprint(api_bp)
    
    # Centralized Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"erro": "Erro interno no servidor", "sucesso": False}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Initialize DB connection and schema
    db.get_connection()
    
    print("=" * 50)
    print("SERVIDOR REFATORADO INICIADO")
    print("Rodando em http://localhost:5000")
    print("=" * 50)

    app.run(host="0.0.0.0", port=5005, debug=app.config["DEBUG"])
