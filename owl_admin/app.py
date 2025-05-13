# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import os,sys
from flask import Flask
# 在文件顶部添加项目根目录到Python路径
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from owl_system.logging_config import configure_logging
configure_logging()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:flaskpass@db/flaskdb'
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


if __name__ == "__main__":
    app = create_app()
    app.run(
        load_dotenv=False,
        host=app.config.get('SERVER_HOST'),
        port=app.config.get('SERVER_PORT')
    )
    