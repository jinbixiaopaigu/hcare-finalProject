# -*- coding: utf-8 -*-
# @Author  : data-sync

"""
数据同步定时任务
将华为Research数据同步到MySQL数据库
"""

import logging
from datetime import datetime

from owl_system.data_sync.synchronizer import run_sync_job
from owl_common.descriptor.listener import TaskSignalListener
from owl_apscheduler.constant import SchedulerType

logger = logging.getLogger(__name__)

@TaskSignalListener('研究数据同步', interval=30, scheduler_type=SchedulerType.DEFAULT)
def research_data_sync_task(*args, **kwargs):
    """
    研究数据同步任务
    将华为Research的研究数据同步到MySQL数据库
    
    Args:
        *args: 可变参数
        **kwargs: 关键字参数
    
    Returns:
        bool: 任务执行结果
    """
    logger.info("开始执行研究数据同步任务")
    
    try:
        # 执行同步任务
        run_sync_job()
        
        logger.info("研究数据同步任务执行成功")
        return True
    except Exception as e:
        logger.error(f"研究数据同步任务执行失败: {str(e)}")
        return False 