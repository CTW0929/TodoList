from app import db
from datetime import datetime

# 角色模型
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', backref='role', lazy=True)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)  # 默认角色
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.name,
            'created_at': self.created_at.isoformat()
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='pending')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assignee = db.relationship('User', backref='todos', lazy=True)
    # 关系定义
    dependencies = db.relationship('TaskDependency', foreign_keys='TaskDependency.task_id', backref='task', lazy=True)
    dependents = db.relationship('TaskDependency', foreign_keys='TaskDependency.dependency_id', backref='dependency', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'assignee_id': self.assignee_id,
            'assignee': self.assignee.username if self.assignee else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'priority': self.priority,
            'status': self.status,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# 任务依赖关系模型
class TaskDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    dependency_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'dependency_id': self.dependency_id,
            'created_at': self.created_at.isoformat()
        }
