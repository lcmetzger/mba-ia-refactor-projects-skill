from flask import Flask
from flask_cors import CORS
from database import db
from config.settings import Config
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.report_routes import report_bp
from middlewares.error_handler import register_error_handlers
import logging
import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    CORS(app)
    db.init_app(app)
    
    # Error Handlers
    register_error_handlers(app)

    # Blueprints
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)

    @app.route('/health')
    def health():
        return {
            'status': 'ok',
            'timestamp': str(datetime.datetime.now()),
            'database': 'connected' if db.engine else 'error'
        }

    @app.route('/')
    def index():
        return {'message': 'Task Manager API', 'version': '2.0 (MVC)'}

    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
