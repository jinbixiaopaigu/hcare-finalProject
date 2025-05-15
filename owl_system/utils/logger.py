import logging

def get_logger(name=None):
    """
    获取logger实例
    
    Args:
        name: logger名称，默认为None
        
    Returns:
        logging.Logger: logger实例
    """
    if name is None:
        name = __name__
    
    logger = logging.getLogger(name)
    
    # 如果logger没有处理器，添加一个默认的处理器
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # 设置默认日志级别
        logger.setLevel(logging.INFO)
    
    return logger
