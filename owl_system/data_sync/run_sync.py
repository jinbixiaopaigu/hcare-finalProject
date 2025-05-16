# -*- coding: utf-8 -*-
# @Author  : data-sync

"""
简单的同步执行脚本
可以直接运行这个脚本来执行同步任务
"""

import logging
import argparse
from typing import Optional

from owl_system.data_sync.synchronizer import DataSynchronizer, run_sync_job

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def sync_specific_table(table_key: str) -> None:
    """同步指定的表
    
    Args:
        table_key: 表配置的键名
    """
    logger.info(f"开始同步表 {table_key}")
    
    # 初始化同步器
    synchronizer = DataSynchronizer()
    
    # 检查表是否存在
    if table_key not in synchronizer.config.tables:
        logger.error(f"未找到表 {table_key} 的配置")
        return
    
    # 执行同步
    inserted, updated = synchronizer.synchronize_table(table_key)
    
    logger.info(f"同步完成：插入 {inserted} 条记录，更新 {updated} 条记录")
    
    # 关闭资源
    synchronizer.close()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='华为Research数据同步脚本')
    parser.add_argument('--table', type=str, help='要同步的表名，如不指定则同步所有表')
    
    args = parser.parse_args()
    
    if args.table:
        sync_specific_table(args.table)
    else:
        logger.info("开始同步所有表")
        run_sync_job()
        logger.info("同步任务完成")

if __name__ == "__main__":
    main()