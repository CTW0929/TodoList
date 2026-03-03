import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 从环境变量获取SECRET_KEY，确保安全
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-development-only'
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 生产环境配置
    DEBUG = False
    TESTING = False
    # 服务器配置
    SERVER_NAME = os.environ.get('SERVER_NAME')
    # 会话配置
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass
