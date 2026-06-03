from database import db
from datetime import datetime
from passlib.hash import argon2

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'active': self.active,
            'created_at': str(self.created_at)
        }
        if include_sensitive:
            data['password'] = self.password
        return data

    def set_password(self, pwd):
        self.password = argon2.hash(pwd)

    def check_password(self, pwd):
        try:
            return argon2.verify(pwd, self.password)
        except:
            return False

    def is_admin(self):
        return self.role == 'admin'
