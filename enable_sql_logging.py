import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

print("SQLAlchemy查询日志已启用，请重启服务生效")