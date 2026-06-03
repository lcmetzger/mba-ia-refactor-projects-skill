from flask import jsonify, request
from models.task import Task
from models.user import User
from models.category import Category
from database import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ReportController:
    @staticmethod
    def summary():
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        tasks_by_status = {
            'pending': Task.query.filter_by(status='pending').count(),
            'in_progress': Task.query.filter_by(status='in_progress').count(),
            'done': Task.query.filter_by(status='done').count(),
            'cancelled': Task.query.filter_by(status='cancelled').count(),
        }

        overdue_tasks = [t.to_dict() for t in Task.query.all() if t.is_overdue()]

        report = {
            'generated_at': str(datetime.utcnow()),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': tasks_by_status,
            'overdue_count': len(overdue_tasks),
            'overdue_tasks': overdue_tasks
        }
        return jsonify(report), 200

    @staticmethod
    def user_productivity():
        users = User.query.all()
        stats = []
        for u in users:
            total = len(u.tasks)
            completed = sum(1 for t in u.tasks if t.status == 'done')
            stats.append({
                'user_id': u.id,
                'user_name': u.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
            })
        return jsonify(stats), 200

    @staticmethod
    def list_categories():
        categories = Category.query.all()
        return jsonify([c.to_dict() for c in categories]), 200

    @staticmethod
    def create_category():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        category = Category(
            name=data['name'],
            description=data.get('description'),
            color=data.get('color', '#000000')
        )
        try:
            db.session.add(category)
            db.session.commit()
            return jsonify(category.to_dict()), 201
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao criar categoria'}), 500
            
    @staticmethod
    def update_category(cat_id):
        cat = Category.query.get(cat_id)
        if not cat: return jsonify({'error': 'Não encontrado'}), 404
        data = request.get_json()
        if 'name' in data: cat.name = data['name']
        if 'description' in data: cat.description = data['description']
        if 'color' in data: cat.color = data['color']
        try:
            db.session.commit()
            return jsonify(cat.to_dict()), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao atualizar'}), 500

    @staticmethod
    def delete_category(cat_id):
        cat = Category.query.get(cat_id)
        if not cat: return jsonify({'error': 'Não encontrado'}), 404
        try:
            db.session.delete(cat)
            db.session.commit()
            return jsonify({'message': 'Deletada'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao deletar'}), 500
