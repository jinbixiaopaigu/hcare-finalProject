"""基础日志配置模块"""

def configure_logging(app):
    """配置应用日志（当前为占位实现）"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.info("日志系统已初始化")