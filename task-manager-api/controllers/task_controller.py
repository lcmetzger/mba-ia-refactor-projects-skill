from flask import jsonify, request
from models.task import Task
from models.user import User
from models.category import Category
from database import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks]), 200

    @staticmethod
    def get_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404
        return jsonify(task.to_dict()), 200

    @staticmethod
    def create_task():
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Título é obrigatório'}), 400

        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 3),
            user_id=data.get('user_id'),
            category_id=data.get('category_id'),
            tags=','.join(data['tags']) if isinstance(data.get('tags'), list) else data.get('tags')
        )

        if data.get('due_date'):
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except:
                return jsonify({'error': 'Formato de data inválido (YYYY-MM-DD)'}), 400

        try:
            db.session.add(task)
            db.session.commit()
            logger.info(f"Task criada: {task.id}")
            return jsonify(task.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar task: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    @staticmethod
    def update_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404
        
        data = request.get_json()
        if 'title' in data: task.title = data['title']
        if 'description' in data: task.description = data['description']
        if 'status' in data: task.status = data['status']
        if 'priority' in data: task.priority = data['priority']
        if 'user_id' in data: task.user_id = data['user_id']
        if 'category_id' in data: task.category_id = data['category_id']
        if 'tags' in data: 
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        if 'due_date' in data:
            if data['due_date']:
                try: task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except: return jsonify({'error': 'Data inválida'}), 400
            else:
                task.due_date = None

        try:
            db.session.commit()
            return jsonify(task.to_dict()), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao atualizar'}), 500

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deletada'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': 'Erro ao deletar'}), 500
            
    @staticmethod
    def search():
        q = request.args.get('q', '')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Task.query
        if q:
            query = query.filter(db.or_(Task.title.contains(q), Task.description.contains(q)))
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == int(priority))
            
        return jsonify([t.to_dict() for t in query.all()]), 200
