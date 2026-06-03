from flask import jsonify, request
from models.user import User
from models.task import Task
from database import db
import logging

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def list_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return jsonify(data), 200

    @staticmethod
    def create_user():
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({'error': 'Dados incompletos'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 409

        user = User(name=data['name'], email=data['email'], role=data.get('role', 'user'))
        user.set_password(data['password'])

        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"Usuário criado: {user.id}")
            return jsonify(user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    @staticmethod
    def login():
        data = request.get_json()
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Email e senha obrigatórios'}), 400

        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Credenciais inválidas'}), 401

        if not user.active:
            return jsonify({'error': 'Usuário inativo'}), 403

        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': f'fake-jwt-token-{user.id}'
        }), 200
        
    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        if 'name' in data: user.name = data['name']
        if 'email' in data: user.email = data['email']
        if 'password' in data: user.set_password(data['password'])
        if 'role' in data: user.role = data['role']
        if 'active' in data: user.active = data['active']
        
        try:
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao atualizar'}), 500

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Usuário deletado'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao deletar'}), 500
