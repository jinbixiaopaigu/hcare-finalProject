# -*- coding: utf-8 -*-
# @Author  : data-sync

import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from owl_system.data_sync.config import SyncConfig, TableMapping
from owl_system.data_sync.research_client import ResearchClient
from owl_system.data_sync.mysql_client import MySQLClient

logger = logging.getLogger(__name__)

class DataSynchronizer:
    """数据同步控制器"""
    
    def __init__(self, config: Optional[SyncConfig] = None, config_file: str = 'config.ini'):
        """初始化同步控制器
        
        Args:
            config: 同步配置，如果未提供则从配置文件加载
            config_file: 配置文件路径，当config为None时使用
        """
        self.config = config or SyncConfig.from_config_file(config_file)
        self.research_client = ResearchClient(self.config)
        self.mysql_client = MySQLClient(self.config)
    
    def synchronize_table(self, table_key: str) -> Tuple[int, int]:
        """同步指定表
        
        Args:
            table_key: 表配置的键名
            
        Returns:
            Tuple[int, int]: 插入和更新的记录数
        """
        if table_key not in self.config.tables:
            logger.error(f"未找到表 {table_key} 的配置")
            return 0, 0
        
        table_mapping = self.config.tables[table_key]
        if not table_mapping.enabled:
            logger.info(f"表 {table_key} 已禁用同步")
            return 0, 0
        
        logger.info(f"开始同步表 {table_mapping.mysql_table_name}")
        
        # 查询Research数据
        research_data = self.research_client.query_data(
            table_id=table_mapping.research_table_id,
            last_sync_time=table_mapping.last_sync_time,
            limit=self.config.batch_size
        )
        
        # 如果没有数据，直接返回
        if not research_data:
            logger.warning(f"没有从Research表 {table_mapping.research_table_id} 获取到数据，可能是限制或表为空")
            return 0, 0
        
        # 转换字段
        mysql_records = self.convert_records(research_data, table_mapping)
        
        # 同步到MySQL
        inserted, updated = self.mysql_client.upsert_records(
            table_name=table_mapping.mysql_table_name,
            records=mysql_records,
            primary_key=table_mapping.primary_key
        )
        
        # 更新上次同步时间
        if research_data:
            latest_record = max(research_data, key=lambda x: x.get('uploadtime', 0))
            upload_time = latest_record.get('uploadtime')
            if upload_time:
                # 将时间戳转换为ISO格式字符串
                if isinstance(upload_time, (int, float)):
                    dt = datetime.fromtimestamp(upload_time / 1000.0)  # 毫秒转为秒
                    table_mapping.last_sync_time = dt.isoformat()
                else:
                    table_mapping.last_sync_time = str(upload_time)
        
        logger.info(f"表 {table_mapping.mysql_table_name} 同步完成: 插入 {inserted} 条，更新 {updated} 条")
        logger.info(f"从Research表 {table_mapping.research_table_id} 获取到 {len(research_data)} 条记录")
        logger.info(f"第一条记录: {research_data[0]}")
        return inserted, updated
    
    def convert_records(self, research_records: List[Dict[str, Any]], table_mapping: TableMapping) -> List[Dict[str, Any]]:
        """转换记录，将Research字段名映射为MySQL字段名
        
        Args:
            research_records: Research数据记录
            table_mapping: 表映射配置
            
        Returns:
            转换后的记录列表
        """
        mysql_records = []
        field_mappings = table_mapping.field_mappings
        
        for record in research_records:
            mysql_record = {}
            
            # 使用字段映射转换字段
            for research_field, mysql_field in field_mappings.items():
                if research_field in record:
                    value = record[research_field]
                    
                    # 特殊处理时间字段
                    if mysql_field in ['upload_time', 'data_time'] and isinstance(value, (int, float)):
                        # 将毫秒时间戳转换为datetime
                        dt = datetime.fromtimestamp(value / 1000.0)
                        mysql_record[mysql_field] = dt
                    else:
                        mysql_record[mysql_field] = value
            
            mysql_records.append(mysql_record)
        
        return mysql_records
    
    def synchronize_all_tables(self) -> Dict[str, Tuple[int, int]]:
        """同步所有启用的表
        
        Returns:
            Dict[str, Tuple[int, int]]: 表名和同步结果（插入数, 更新数）的映射
        """
        results = {}
        
        for table_key, table_mapping in self.config.tables.items():
            if table_mapping.enabled:
                try:
                    inserted, updated = self.synchronize_table(table_key)
                    results[table_key] = (inserted, updated)
                except Exception as e:
                    logger.error(f"同步表 {table_key} 时出错: {str(e)}")
                    results[table_key] = (0, 0)
        
        return results
    
    def close(self):
        """关闭数据库连接"""
        self.mysql_client.close()


def run_sync_job(config_file: str = 'config.ini'):
    """运行同步任务
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        bool: 同步是否成功
    """
    try:
        logger.info(f"开始执行数据同步任务，使用配置文件 {config_file}")
        
        # 初始化同步器
        synchronizer = DataSynchronizer(config_file=config_file)
        
        # 同步所有表
        results = synchronizer.synchronize_all_tables()
        
        # 输出同步结果
        total_inserted = 0
        total_updated = 0
        
        for table_key, (inserted, updated) in results.items():
            total_inserted += inserted
            total_updated += updated
            
            if inserted > 0 or updated > 0:
                logger.info(f"表 {table_key} 同步结果: 插入 {inserted} 条，更新 {updated} 条")
        
        logger.info(f"数据同步任务完成: 总共插入 {total_inserted} 条，更新 {total_updated} 条")
        
        # 关闭连接
        synchronizer.close()
        
        return True
    except Exception as e:
        logger.error(f"数据同步任务执行失败: {str(e)}")
        return False


if __name__ == "__main__":
    run_sync_job() 