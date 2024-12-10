# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import os,sys
from flask import Flask 

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
        
    owl.init_app(app,PROJECT_ROOT)
    cors.init_app(app)
    fredis.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    
    app_completed.send(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        load_dotenv=False,
        host=app.config.get('SERVER_HOST'),
        port=app.config.get('SERVER_PORT')
    )
    