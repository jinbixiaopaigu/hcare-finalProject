# -*- coding: utf-8 -*-
# @Author  : data-sync

import logging
from typing import Dict, List, Any, Optional, Tuple

import pymysql
from pymysql.cursors import DictCursor

from owl_system.data_sync.config import SyncConfig, TableMapping

logger = logging.getLogger(__name__)

class MySQLClient:
    """MySQL数据库客户端"""
    
    def __init__(self, config: SyncConfig):
        """初始化客户端"""
        self.config = config
        self.connection = None
        # 打印配置信息，不包含密码
        logger.info(f"MySQL配置: 主机={config.mysql_host}, 端口={config.mysql_port}, 用户={config.mysql_user}, 数据库={config.mysql_db}")
        # 检查密码是否为空
        if not config.mysql_password:
            logger.warning("MySQL密码为空，这可能导致连接失败")
        self._connect()
    
    def _connect(self):
        """连接数据库"""
        try:
            # 打印详细配置信息用于调试
            logger.info(f"尝试连接MySQL数据库: {self.config.mysql_host}:{self.config.mysql_port}, 用户: {self.config.mysql_user}")
            if self.config.mysql_password:
                logger.info("使用配置的密码进行连接")
            else:
                logger.warning("没有配置密码，尝试无密码连接")
                
            self.connection = pymysql.connect(
                host=self.config.mysql_host,
                port=self.config.mysql_port,
                user=self.config.mysql_user,
                password=self.config.mysql_password,
                database=self.config.mysql_db,
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            logger.info("MySQL数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise
    
    def get_table_schema(self, table_name: str) -> Dict[str, Dict[str, Any]]:
        """获取表结构
        
        Args:
            table_name: 表名
            
        Returns:
            表结构字典 {字段名: {信息}}
        """
        schema = {}
        try:
            with self.connection.cursor() as cursor:
                # 查询表结构
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, COLUMN_KEY, IS_NULLABLE, COLUMN_COMMENT
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                """, (self.config.mysql_db, table_name))
                
                for row in cursor.fetchall():
                    column_name = row['COLUMN_NAME']
                    schema[column_name] = {
                        'data_type': row['DATA_TYPE'],
                        'is_primary': row['COLUMN_KEY'] == 'PRI',
                        'is_nullable': row['IS_NULLABLE'] == 'YES',
                        'comment': row['COLUMN_COMMENT']
                    }
            
            return schema
        except Exception as e:
            logger.error(f"获取表 {table_name} 结构失败: {str(e)}")
            return {}
    
    def upsert_records(self, table_name: str, records: List[Dict[str, Any]], primary_key: str = 'id') -> Tuple[int, int]:
        """插入或更新记录
        
        Args:
            table_name: 表名
            records: 记录列表
            primary_key: 主键字段名
            
        Returns:
            插入和更新的记录数元组
        """
        if not records:
            logger.info("没有记录需要更新，直接返回")
            return 0, 0
        
        inserted_count = 0
        updated_count = 0
        
        try:
            # 获取第一条记录的字段列表，假设所有记录的字段一致
            example_record = records[0]
            fields = list(example_record.keys())
            
            # 检查表结构
            table_schema = self.get_table_schema(table_name)
            if not table_schema:
                logger.error(f"表 {table_name} 不存在或无法获取结构")
                return 0, 0
            
            # 检查字段是否存在于表中
            valid_fields = [field for field in fields if field in table_schema]
            if not valid_fields:
                logger.error(f"表 {table_name} 没有有效的字段可以插入，字段映射可能有误")
                logger.info(f"记录字段: {fields}")
                logger.info(f"表字段: {list(table_schema.keys())}")
                return 0, 0
            
            # 检查主键是否有效
            if primary_key not in table_schema:
                logger.error(f"主键 {primary_key} 不在表 {table_name} 的字段中")
                return 0, 0
            
            # 分批处理记录，避免一次插入过多数据
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                
                # 构建插入SQL
                fields_str = ", ".join(valid_fields)
                placeholders = ", ".join(["%s"] * len(valid_fields))
                
                # 构建更新SQL部分
                update_parts = [f"{field} = VALUES({field})" for field in valid_fields if field != primary_key]
                
                # 如果没有可更新字段，手动添加一个空更新以避免SQL错误
                if not update_parts:
                    logger.warning(f"表 {table_name} 没有可更新字段，仅有主键 {primary_key}")
                    update_parts = [f"{primary_key} = VALUES({primary_key})"]
                    
                update_str = ", ".join(update_parts)
                
                sql = f"""
                    INSERT INTO {table_name} ({fields_str})
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {update_str}
                """
                
                logger.debug(f"执行SQL: {sql}")
                
                # 准备参数
                params = []
                for record in batch:
                    row_values = []
                    for field in valid_fields:
                        value = record.get(field)
                        # 检查数据类型兼容性
                        if field in table_schema:
                            data_type = table_schema[field]['data_type']
                            # 特殊处理某些类型
                            if data_type in ('datetime', 'timestamp') and isinstance(value, (int, float)):
                                # 已经在synchronizer中处理了时间戳转换
                                pass
                        row_values.append(value)
                    params.append(tuple(row_values))
                
                # 为调试打印第一条记录的值
                if params:
                    logger.debug(f"第一条记录: 字段={valid_fields}, 值={params[0]}")
                
                # 执行批量插入
                try:
                    with self.connection.cursor() as cursor:
                        # 先尝试单条插入以确认SQL有效
                        if params:
                            try:
                                logger.debug(f"尝试单条插入验证SQL...")
                                single_sql = f"""
                                    INSERT INTO {table_name} ({fields_str})
                                    VALUES ({placeholders})
                                    ON DUPLICATE KEY UPDATE {update_str}
                                """
                                cursor.execute(single_sql, params[0])
                                logger.debug("单条插入验证成功")
                                # 回滚单条插入
                                self.connection.rollback()
                            except Exception as e:
                                logger.error(f"单条插入验证失败: {str(e)}")
                                # 继续尝试执行批量插入
                        
                        # 执行批量插入
                        inserted = cursor.executemany(sql, params)
                        self.connection.commit()
                        
                        # 统计插入和更新数量
                        # executemany 返回的是受影响的行数，每条记录在插入时是1，更新时是2
                        affected_rows = inserted
                        if affected_rows > 0:
                            logger.info(f"影响行数: {affected_rows}")
                            updates = affected_rows // 2
                            inserts = affected_rows - updates
                            inserted_count += inserts
                            updated_count += updates
                            logger.info(f"批次处理完成: 插入 {inserts} 条，更新 {updates} 条")
                except pymysql.Error as e:
                    logger.error(f"SQL执行错误: {str(e)}")
                    logger.error(f"错误代码: {e.args[0]}, 错误消息: {e.args[1] if len(e.args) > 1 else 'Unknown'}")
                    # 失败后尝试逐条插入以定位问题
                    if params:
                        logger.info("尝试逐条插入以定位问题...")
                        success_count = 0
                        for idx, param in enumerate(params):
                            try:
                                with self.connection.cursor() as cursor:
                                    cursor.execute(sql, param)
                                    self.connection.commit()
                                    success_count += 1
                            except Exception as single_e:
                                logger.error(f"第 {idx+1} 条记录插入失败: {str(single_e)}")
                                logger.debug(f"记录内容: {param}")
                        logger.info(f"逐条插入: 成功 {success_count}/{len(params)} 条")
                    raise
            
            logger.info(f"表 {table_name} 数据更新完成: 总共插入 {inserted_count} 条，更新 {updated_count} 条")
            return inserted_count, updated_count
        
        except Exception as e:
            logger.error(f"插入或更新记录失败: {str(e)}")
            if hasattr(e, '__traceback__'):
                import traceback
                logger.error(traceback.format_exc())
            self.connection.rollback()
            return 0, 0
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close() 