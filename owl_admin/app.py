# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import os
import sys  # 添加sys模块
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def load_env():
    """加载.env文件并返回环境变量字典"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    print(f"正在加载环境变量文件: {env_path}")
    env_dict = {}
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                    env_dict[key] = value
    return env_dict

# 加载环境变量
env_vars = load_env()

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)  # 修复sys未定义

# 初始化数据库扩展
db = SQLAlchemy()

app = Flask(__name__, static_folder=None)

try:
    # 优先从环境变量获取配置
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'FLASK_SQLALCHEMY_DATABASE_URI', 
        'mysql+pymysql://root:q1w2e3r4@localhost/hcare-final'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        'FLASK_SQLALCHEMY_TRACK_MODIFICATIONS', 
        False
    )
    
    # 初始化数据库
    db.init_app(app)
    
except Exception as e:
    print(f"[警告] 使用环境变量配置失败，回退到默认配置: {str(e)}")
    app.config.from_pyfile('config/app.yml')

# 输出当前配置
def print_current_config():
    """打印当前应用配置"""
    print("\n=== 当前应用配置 ===")
    print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"跟踪修改: {app.config['SQLALCHEMY_TRACK_MODIFICATIONS']}")
    # print(f"服务器配置: {app.config['host']}:{app.config['port']}")  # 显示实际端口
    # print(f"环境变量: {dict(os.environ)}")
    print("====================\n")


def create_app() -> Flask:
    """
    创建flask应用
    
    Returns:
        Flask: flask应用
    """
    from owl_admin.ext import db,fredis,lm,cors,owl
    from owl_common.base.signal import app_completed

    app = Flask(__name__,static_folder=None)
    
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:q1w2e3r4@127.0.0.1/hcare-final'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 优先初始化数据库
    print("初始化数据库...")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # 初始化其他插件
    print("初始化核心插件...")
    owl.init_app(app,PROJECT_ROOT)
    cors.init_app(app)
    # 恢复Redis初始化
    fredis.init_app(app) 
    lm.init_app(app)
    
    # 强制注册医疗模块
    from owl_system.modules.medical import register_medical_module
    register_medical_module(app)
    
    app_completed.send(app)
    
    # 打印所有注册的路由
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods}: {rule}")
    
    return app

# 配置日志
# try:
#     from owl_system.logging_config import configure_logging
#     configure_logging(app)
# except ImportError as e:
#     print(f"[警告] 日志模块加载失败: {str(e)}")

if __name__ == '__main__':
    app=create_app()
    print_current_config()
    # 显式使用配置中的端口启动
    app.run(
        debug=True,
        host=app.config.get('host', 'localhost'),
        port=int(app.config.get('port', 8000))  # 确保使用配置端口
    )
