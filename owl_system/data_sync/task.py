# -*- coding: utf-8 -*-
# @Author  : data-sync

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from owl_system.data_sync.config import SyncConfig
from owl_system.data_sync.synchronizer import DataSynchronizer, run_sync_job

logger = logging.getLogger(__name__)

class SyncTask:
    """同步任务管理器"""
    
    def __init__(self, config_file: str = 'config.ini'):
        """初始化任务管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = SyncConfig.from_config_file(config_file)
        self.scheduler = BackgroundScheduler()
        self.job = None
    
    def start(self):
        """启动定时任务"""
        # 创建定时触发器
        trigger = IntervalTrigger(minutes=self.config.sync_interval)
        
        # 添加任务
        self.job = self.scheduler.add_job(
            run_sync_job,
            trigger=trigger,
            id='data_sync_job',
            name='研究数据同步任务',
            args=[self.config_file],  # 传递配置文件路径
            replace_existing=True
        )
        
        # 启动调度器
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info(f"定时同步任务已启动，间隔 {self.config.sync_interval} 分钟")
    
    def stop(self):
        """停止定时任务"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("定时同步任务已停止")


# 全局任务管理器实例
sync_task_manager = None


def init_scheduler(config_file: str = 'config.ini'):
    """初始化并启动调度器
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        调度器实例
    """
    global sync_task_manager
    sync_task_manager = SyncTask(config_file)
    sync_task_manager.start()
    return sync_task_manager.scheduler


def shutdown_scheduler():
    """关闭调度器"""
    global sync_task_manager
    if sync_task_manager:
        sync_task_manager.stop()


def run_sync_now(config_file: str = 'config.ini'):
    """立即执行一次同步任务
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        同步是否成功
    """
    logger.info("立即执行同步任务")
    return run_sync_job(config_file) 