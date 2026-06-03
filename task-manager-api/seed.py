from app import create_app
from database import db
from models.user import User
from models.category import Category
from models.task import Task
from datetime import datetime, timedelta

app = create_app()

def seed():
    with app.app_context():
        # Clean up
        db.drop_all()
        db.create_all()

        # Users
        admin = User(name='Admin', email='admin@task.com', role='admin')
        admin.set_password('admin123')
        
        user1 = User(name='John Doe', email='john@task.com', role='user')
        user1.set_password('user123')

        db.session.add_all([admin, user1])
        db.session.commit()

        # Categories
        work = Category(name='Work', description='Work related tasks', color='#FF0000')
        personal = Category(name='Personal', description='Personal tasks', color='#00FF00')
        db.session.add_all([work, personal])
        db.session.commit()

        # Tasks
        t1 = Task(
            title='Refactor API',
            description='Refactor the API to MVC architecture',
            status='in_progress',
            priority=1,
            user_id=user1.id,
            category_id=work.id,
            due_date=datetime.utcnow() + timedelta(days=2)
        )
        
        t2 = Task(
            title='Buy groceries',
            description='Milk, bread, eggs',
            status='pending',
            priority=3,
            user_id=user1.id,
            category_id=personal.id,
            due_date=datetime.utcnow() - timedelta(days=1)
        )

        db.session.add_all([t1, t2])
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
