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
    
    def sync_data(self, table_key: str) -> Dict[str, Any]:
        """同步指定表的数据
        
        Args:
            table_key: 表配置的键名
            
        Returns:
            Dict[str, Any]: 同步结果，包含success、message、inserted和updated字段
        """
        try:
            logger.info(f"开始同步表 {table_key}")
            logger.info(f"可用的表配置: {list(self.config.tables.keys())}")
            
            if table_key not in self.config.tables:
                error_msg = f"未找到表 {table_key} 的配置"
                logger.error(error_msg)
                return {
                    'success': False,
                    'message': error_msg,
                    'inserted': 0,
                    'updated': 0
                }
            
            table_mapping = self.config.tables[table_key]
            logger.info(f"获取到表映射配置: {table_mapping}")
            
            if not table_mapping.enabled:
                message = f"表 {table_key} 已禁用同步"
                logger.info(message)
                return {
                    'success': True,
                    'message': message,
                    'inserted': 0,
                    'updated': 0
                }
            
            inserted, updated = self.synchronize_table(table_key)
            
            if inserted > 0 or updated > 0:
                message = f"同步成功：插入 {inserted} 条记录，更新 {updated} 条记录"
                logger.info(message)
                return {
                    'success': True,
                    'message': message,
                    'inserted': inserted,
                    'updated': updated
                }
            else:
                message = "没有新数据需要同步"
                logger.info(message)
                return {
                    'success': True,
                    'message': message,
                    'inserted': 0,
                    'updated': 0
                }
        except Exception as e:
            error_msg = f"同步失败：{str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'message': error_msg,
                'inserted': 0,
                'updated': 0
            }
    
    def _print_field_structure(self, record: Dict[str, Any], prefix: str = "", indent: str = "  "):
        """递归打印记录的字段结构
        
        Args:
            record: 数据记录
            prefix: 字段前缀（用于嵌套字段）
            indent: 缩进字符串
        """
        for key, value in record.items():
            full_key = f"{prefix}.{key}" if prefix else key
            value_type = type(value).__name__
            
            if isinstance(value, dict):
                print(f"{indent}- {key} (嵌套对象, 类型: {value_type})")
                self._print_field_structure(value, full_key, indent + "  ")
            else:
                print(f"{indent}- {key} (类型: {value_type})")
                
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
        
        # 确保打印表名和研究表ID，无论是否有数据
        print(f"\n== 准备同步表 {table_mapping.mysql_table_name} ==")
        print(f"研究表ID: {table_mapping.research_table_id}")
        
        try:
            # 查询Research数据
            research_data = self.research_client.query_data(
                table_id=table_mapping.research_table_id,
                last_sync_time=table_mapping.last_sync_time,
                limit=self.config.batch_size
            )
            
            # 如果没有数据，直接返回
            if not research_data:
                print(f"\n未从华为Research表 {table_mapping.research_table_id} 获取到数据")
                print("可能原因:")
                print("1. 表中没有数据")
                print("2. 表ID不正确")
                print("3. 全部数据已同步")
                logger.warning(f"没有从Research表 {table_mapping.research_table_id} 获取到数据，可能是限制或表为空")
                return 0, 0
            
            # 打印数据统计信息
            print(f"\n== 华为Research表 {table_mapping.research_table_id} 数据统计 ==")
            print(f"获取记录数: {len(research_data)} 条")
            
            # 打印表字段结构
            if research_data:
                first_record = research_data[0]
                print("\n字段结构:")
                self._print_field_structure(first_record)
            
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
            
            # 打印字段映射信息
            print("\n字段映射关系:")
            for research_field, mysql_field in table_mapping.field_mappings.items():
                print(f"  - {research_field} => {mysql_field}")
            
            # 打印同步结果
            print(f"\n同步结果: 插入 {inserted} 条，更新 {updated} 条记录\n")
            
            return inserted, updated
            
        except Exception as e:
            error_msg = f"同步表 {table_mapping.mysql_table_name} 出错: {str(e)}"
            print(f"\n错误: {error_msg}")
            logger.error(error_msg)
            return 0, 0
    
    def get_nested_value(self, record: Dict[str, Any], field_path: str) -> Any:
        """从嵌套字典中获取值
        
        Args:
            record: 数据记录
            field_path: 字段路径，例如 "oxygenSaturation.oxygenSaturation.value"
            
        Returns:
            字段值或None（如果路径不存在）
        """
        if '.' not in field_path:
            return record.get(field_path)
        
        parts = field_path.split('.')
        current = record
        
        try:
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            return current
        except (KeyError, TypeError):
            return None
    
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
        
        # 添加调试输出：显示前两条记录的原始数据和嵌套结构
        if research_records and len(research_records) > 0:
            print("\n== 调试输出：前两条记录的字段值 ==")
            for i, record in enumerate(research_records[:2]):  # 只处理前两条记录
                print(f"\n记录 {i+1}:")
                
                # 识别并显示主要嵌套结构
                for key, value in record.items():
                    if isinstance(value, dict):
                        print(f"  {key} 结构:")
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, dict):
                                print(f"    - {subkey}: {subvalue}")
                            else:
                                print(f"    - {subkey}: {subvalue}")
                
                # 检查一些主要字段的值（通用方式）
                for field_path, field_name in field_mappings.items():
                    if "." in field_path and "value" in field_path:  # 只显示带值的嵌套字段
                        value = self.get_nested_value(record, field_path)
                        if value is not None:
                            unit_path = field_path.replace(".value", ".unit")
                            unit = self.get_nested_value(record, unit_path)
                            print(f"  {field_path} => {field_name}: {value} {unit}")
                
        for record in research_records:
            mysql_record = {}
            
            # 使用字段映射转换字段
            for research_field, mysql_field in field_mappings.items():
                # 判断是否为嵌套字段
                if '.' in research_field:
                    value = self.get_nested_value(record, research_field)
                elif research_field in record:
                    value = record[research_field]
                else:
                    continue
                
                # 如果值存在，进行处理
                if value is not None:
                    # 特殊处理时间字段
                    if mysql_field in ['upload_time', 'data_time', 'measurement_time'] and isinstance(value, (int, float)):
                        # 将毫秒时间戳转换为datetime
                        dt = datetime.fromtimestamp(value / 1000.0)
                        mysql_record[mysql_field] = dt
                    else:
                        mysql_record[mysql_field] = value
            
            # 记录转换日志
            if mysql_record:
                logger.debug(f"转换记录: {mysql_record}")
            else:
                logger.warning(f"记录转换失败: {record}")
            
            mysql_records.append(mysql_record)
        
        # 添加额外调试输出：显示前两条MySQL记录
        if mysql_records and len(mysql_records) > 0:
            print("\n== 调试输出：前两条MySQL记录 ==")
            for i, record in enumerate(mysql_records[:2]):
                print(f"\n记录 {i+1}:")
                print(f"  id: {record.get('id')}")
                print(f"  user_id: {record.get('user_id')}")
                print(f"  data_time: {record.get('data_time')}")
                
                # 动态显示表中的字段（而不是硬编码血氧字段）
                for field_name in field_mappings.values():
                    if field_name not in ['id', 'user_id', 'data_time'] and field_name in record:
                        value = record.get(field_name)
                        if value is not None:
                            print(f"  {field_name}: {value}")
        
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