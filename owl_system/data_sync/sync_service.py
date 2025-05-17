import logging
import importlib
from flask import jsonify
from dataclasses import dataclass

from owl_system.data_sync.synchronizer import DataSynchronizer
from owl_system.utils.response_utils import success, error

logger = logging.getLogger(__name__)

def sync_data_by_model_name(model_name):
    """
    根据模型名称同步数据
    
    Args:
        model_name (str): 模型名称，例如 'BloodOxygenSaturation'
        
    Returns:
        flask.Response: 包含同步结果的响应
    """
    try:
        logger.info(f"开始同步模型: {model_name}")
        
        # 将CamelCase转换为snake_case
        table_name = ''.join(['_'+c.lower() if c.isupper() else c for c in model_name]).lstrip('_')
        
        # 初始化同步器
        synchronizer = DataSynchronizer(config_file='config.ini')
        
        # 检查表是否存在
        if table_name not in synchronizer.config.tables:
            return error(message=f"{model_name}数据同步失败，未找到表映射配置")
        
        # 执行同步
        inserted, updated = synchronizer.synchronize_table(table_name)
        
        # 关闭连接
        synchronizer.close()
        
        return success(message=f"{model_name}数据同步成功", data={
            "added": inserted,
            "updated": updated
        })
    except Exception as e:
        logger.error(f"同步{model_name}数据时出错: {str(e)}", exc_info=True)
        return error(message=f"同步{model_name}数据时出错: {str(e)}", code=500) 