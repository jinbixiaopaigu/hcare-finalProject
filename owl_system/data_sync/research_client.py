# -*- coding: utf-8 -*-
# @Author  : data-sync

import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Union

from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import (
    SearchTableDataRequest, 
    FilterCondition, 
    FilterOperatorType,
    FilterLogicType
)

from owl_system.data_sync.config import SyncConfig, TableMapping

logger = logging.getLogger(__name__)

class ResearchClient:
    """华为Research数据库客户端"""
    
    def __init__(self, config: SyncConfig):
        """初始化客户端"""
        self.config = config
        self.bridge_config = BridgeConfig(
            config.research_env,
            config.research_access_key,
            config.research_secret_key
        )
        self.http_config = HttpClientConfig(
            config.connect_timeout,
            config.read_timeout,
            config.retry_on_fail
        )
        
        logger.info(f"初始化华为Research客户端，Access Key: {config.research_access_key[:4]}...{config.research_access_key[-4:]}")
        self.bridge_client = BridgeClient(self.bridge_config, self.http_config)
        
        # 获取项目ID（如果尚未设置）
        if not config.project_id:
            self._init_project_info()
        
        logger.info(f"华为Research客户端初始化成功，项目ID: {config.project_id}")
    
    def _init_project_info(self):
        """初始化项目信息"""
        try:
            logger.info("获取项目信息...")
            projects = self.bridge_client.get_bridgedata_provider().list_projects()
            
            if not projects:
                logger.warning("未找到任何项目，无法进行数据同步")
                return
            
            # 使用第一个项目
            project = projects[0]
            self.config.project_id = project.get('projectId')
            self.config.project_code = project.get('projectCode')
            
            logger.info(f"成功获取项目信息: ID={self.config.project_id}, Code={self.config.project_code}")
        except Exception as e:
            logger.error(f"获取项目信息失败: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def get_table_schema(self, table_id: str) -> Dict[str, Dict[str, Any]]:
        """获取表结构
        
        Args:
            table_id: 表ID
            
        Returns:
            表结构字典 {字段名: {类型等信息}}
        """
        try:
            logger.info(f"获取表 {table_id} 结构...")
            
            schema = {}
            
            # 构造查询条件，使用EXISTS条件以确保能获取到数据
            condition = [FilterCondition("id", FilterOperatorType.EXISTS, True)]
            
            # 构造查询请求
            req = SearchTableDataRequest(
                table_id, 
                filters=condition, 
                desired_size=1,
                project_id=self.config.project_id
            )
            
            # 标记是否获取到数据
            has_data = [False]
            
            # 定义回调函数
            def schema_callback(rows, total_cnt):
                logger.info(f"表 {table_id} 查询结果: 共 {total_cnt} 条记录，返回 {len(rows) if rows else 0} 条")
                
                if not rows:
                    logger.warning(f"表 {table_id} 中没有数据，无法通过数据获取字段信息")
                    return
                
                has_data[0] = True
                
                # 从第一行数据提取字段信息
                row = rows[0]
                for field_name, value in row.items():
                    field_type = type(value).__name__
                    schema[field_name] = {
                        'type': field_type,
                        'sample': value
                    }
            
            # 执行查询
            self.bridge_client.get_bridgedata_provider().query_table_data(
                req, 
                callback=schema_callback
            )
            
            # 如果没有数据，尝试使用默认字段
            if not has_data[0]:
                logger.info(f"表 {table_id} 中没有数据，使用默认字段结构")
                
                # 根据表ID解析表名，尝试猜测字段
                table_name = table_id.split('_')[-2] if '_' in table_id else table_id
                
                # 为不同类型的表提供默认字段
                if 'atrialfibrillation' in table_name.lower():
                    schema = {
                        'id': {'type': 'str'},
                        'healthid': {'type': 'str'},
                        'recordgroupid': {'type': 'str'},
                        'uploadtime': {'type': 'int'},
                        'recordtime': {'type': 'int'},
                        'atrialfibrillationdetectresult': {'type': 'str'},
                        'atrialfibrillationrisklevel': {'type': 'str'},
                        'externalid': {'type': 'str'},
                        'metadataversion': {'type': 'int'}
                    }
                else:
                    # 通用字段
                    schema = {
                        'id': {'type': 'str'},
                        'healthid': {'type': 'str'},
                        'recordgroupid': {'type': 'str'},
                        'uploadtime': {'type': 'int'},
                        'recordtime': {'type': 'int'},
                        'externalid': {'type': 'str'},
                        'metadataversion': {'type': 'int'}
                    }
                
                logger.info(f"为表 {table_id} 使用默认字段结构: {', '.join(schema.keys())}")
            
            return schema
        except Exception as e:
            logger.error(f"获取表 {table_id} 结构失败: {str(e)}")
            logger.debug(traceback.format_exc())
            return {}
    
    def query_data(
        self, 
        table_id: str, 
        conditions: Optional[List[FilterCondition]] = None,
        include_fields: Optional[List[str]] = None,
        last_sync_time: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """查询数据
        
        Args:
            table_id: 表ID
            conditions: 过滤条件
            include_fields: 包含的字段
            last_sync_time: 上次同步时间，用于增量同步
            limit: 查询限制
            
        Returns:
            查询结果列表
        """
        try:
            logger.info(f"查询表 {table_id} 数据...")
            
            # 准备过滤条件
            if conditions is None:
                conditions = []
            
            # 在构造查询请求之前添加
            logger.info(f"查询条件: {conditions}")
            logger.info(f"项目ID: {self.config.project_id}")
            
            # 如果有上次同步时间，添加时间过滤条件
            if last_sync_time:
                try:
                    # 尝试将字符串时间转换为时间戳
                    dt = datetime.fromisoformat(last_sync_time.replace('Z', '+00:00'))
                    timestamp = int(dt.timestamp() * 1000)  # 转换为毫秒级时间戳
                    
                    logger.info(f"使用上次同步时间: {last_sync_time} (时间戳: {timestamp})")
                    
                    # 添加上传时间条件：大于上次同步时间
                    time_condition = FilterCondition(
                        "uploadtime", 
                        FilterOperatorType.GREATER_THAN, 
                        timestamp
                    )
                    
                    # 如果已有其他条件，使用AND连接
                    if conditions:
                        time_condition.logic = FilterLogicType.AND
                    
                    conditions.append(time_condition)
                except Exception as e:
                    logger.error(f"处理上次同步时间失败: {str(e)}")
                    logger.debug(traceback.format_exc())
            
            # 确保至少有一个条件，避免空条件报错
            if not conditions:
                logger.info("未提供查询条件，使用默认条件")
                conditions = [FilterCondition("uniqueid", FilterOperatorType.EXISTS, True)]
                
            # 构造查询请求
            req = SearchTableDataRequest(
                table_id, 
                filters=conditions,
                desired_size=limit,
                include_fields=include_fields,
                project_id=self.config.project_id
            )
            
            # 保存查询结果
            results = []
            
            # 回调函数，处理查询结果
            def data_callback(rows, total_cnt):
                logger.info(f"表 {table_id} 查询结果: 共 {total_cnt} 条记录，返回 {len(rows) if rows else 0} 条")
                
                if rows:
                    results.extend(rows)
                else:
                    logger.info(f"查询表 {table_id} 成功，但没有匹配的记录")
            
            # 执行查询
            self.bridge_client.get_bridgedata_provider().query_table_data(
                req, 
                callback=data_callback
            )
            
            if results:
                logger.info(f"从表 {table_id} 获取了 {len(results)} 条记录")
                logger.info(f"第一条数据示例: {results[0]}")
            else:
                logger.info(f"表 {table_id} 没有需要同步的新数据")
            
            if not results:
                logger.warning(f"查询表 {table_id} 没有返回任何数据")
            else:
                logger.info(f"查询表 {table_id} 返回 {len(results)} 条数据")
            
            return results
        except Exception as e:
            logger.error(f"查询表 {table_id} 数据失败: {str(e)}")
            logger.debug(traceback.format_exc())
            return []
    
    def get_field_mappings(self, table_mapping: TableMapping) -> Dict[str, str]:
        """获取字段映射
        
        如果没有预定义的映射，会自动尝试匹配字段
        
        Args:
            table_mapping: 表映射配置
            
        Returns:
            字段映射字典 {research字段: mysql字段}
        """
        # 如果已经有映射，直接返回
        if table_mapping.field_mappings:
            logger.info(f"使用预定义的字段映射: {', '.join(table_mapping.field_mappings.keys())}")
            return table_mapping.field_mappings
        
        # 尝试获取表结构信息
        logger.info(f"尝试为表 {table_mapping.research_table_id} 生成自动字段映射...")
        schema = self.get_table_schema(table_mapping.research_table_id)
        if not schema:
            logger.warning(f"无法获取表 {table_mapping.research_table_id} 的结构，使用默认映射")
            return {
                "id": "id",
                "healthid": "user_id",
                "recordgroupid": "group_id",
                "uploadtime": "upload_time",
                "recordtime": "data_time",
                "externalid": "external_id",
                "metadataversion": "metadata_version"
            }
        
        # 创建默认映射
        field_mappings = {}
        for field_name in schema.keys():
            # 转换字段名（驼峰转下划线）
            mysql_field = self._camel_to_snake(field_name)
            field_mappings[field_name] = mysql_field
        
        logger.info(f"自动生成的字段映射: {', '.join(field_mappings.keys())}")
        return field_mappings
    
    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """驼峰命名转下划线命名"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() 