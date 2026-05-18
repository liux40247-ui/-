"""
目标检测评估平台
主应用入口
"""
from flask import Flask, render_template
from config import config


def create_app(config_name='default'):
    """
    应用工厂函数

    Args:
        config_name: 配置名称 ('development', 'production', 'testing')

    Returns:
        Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 注册蓝图
    from blueprints import register_blueprints
    register_blueprints(app)

    # 注册主页路由
    @app.route('/')
    def index():
        """首页"""
        return render_template('index.html')

    # 数据集管理页面
    @app.route('/datasets')
    def dataset_page():
        """数据集管理页面"""
        return render_template('datasets.html')

    # 评估页面
    @app.route('/evaluate')
    def evaluate_page():
        """评估页面"""
        return render_template('evaluation.html')

    # 对比页面
    @app.route('/compare')
    def compare_page():
        """模型对比页面"""
        return render_template('comparison.html')

    # 结果页面
    @app.route('/results')
    def results_page():
        """结果展示页面"""
        return render_template('results.html')

    # 模型管理页面
    @app.route('/models')
    def models_page():
        """模型管理页面"""
        return render_template('models.html')

    # API信息
    @app.route('/api/info')
    def api_info():
        """API信息"""
        return {
            'name': 'Object Detection Evaluation Platform',
            'version': '2.0.0',
            'supported_models': ['YOLOv5', 'YOLOv8'],
            'description': '支持YOLO系列目标检测模型的评估与对比'
        }

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return render_template('index.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('index.html'), 500

    return app


# 创建应用实例（用于直接运行）
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
