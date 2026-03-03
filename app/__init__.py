from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
import os

# 创建应用实例
app = Flask(__name__)

# 加载配置
app.config.from_object('config.ProductionConfig')

# 配置缓存
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# 初始化扩展
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
cache = Cache(app)
csrf = CSRFProtect(app)

# 配置CORS
CORS(app, resources={r"/*": {"origins": ["*"]}})

# 添加安全头部
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# 导入模型和路由
from app import models, routes

# 创建数据库表
with app.app_context():
    db.create_all()
    # 初始化角色数据
    from app.models import Role
    if Role.query.count() == 0:
        user_role = Role(name='user', description='普通用户')
        admin_role = Role(name='admin', description='管理员')
        db.session.add(user_role)
        db.session.add(admin_role)
        db.session.commit()