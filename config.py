"""
Flask配置文件
支持开发环境和生产环境配置
"""
import os
from datetime import timedelta


class Config:
    """基础配置类"""
    # Flask 核心配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # 数据集存储路径 (用于模型评估的图片上传)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MODEL_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'models')
    REPORT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB 最大文件大小

    # 自定义模型存储路径
    CUSTOM_MODELS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'custom_models')
    CUSTOM_MODELS_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'custom_models.sqlite')
    MAX_MODEL_SIZE = 500 * 1024 * 1024  # 500MB 模型文件大小限制

    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    ALLOWED_MODEL_EXTENSIONS = {'pt', 'pth', 'onnx'}

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session 配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 评估缓存目录
    EVALUATION_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'evaluations')

    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 创建必要的目录
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_FOLDER, exist_ok=True)
        os.makedirs(Config.REPORT_FOLDER, exist_ok=True)
        os.makedirs(Config.EVALUATION_CACHE_DIR, exist_ok=True)
        os.makedirs(Config.CUSTOM_MODELS_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')), exist_ok=True)


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
