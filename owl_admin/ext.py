# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from werkzeug.local import LocalProxy
from flask import current_app

from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_cors import CORS
from redis import Redis

from owl_common.owl.extension import FlaskOwl
from owl_common.sqlalchemy.extension import SQLAlchemy
    

owl = FlaskOwl()
cors = CORS()

fredis = FlaskRedis()
redis_cache:Redis = LocalProxy(
    lambda: current_app.extensions["redis"]._redis_client
) 
lm = LoginManager()
db = SQLAlchemy()