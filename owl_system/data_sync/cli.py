# -*- coding: utf-8 -*-
# @Author  : data-sync

import sys
import time
import logging
import argparse
from typing import List, Dict, Any, Optional

from owl_system.data_sync.config import SyncConfig, TableMapping
from owl_system.data_sync.research_client import ResearchClient
from owl_system.data_sync.mysql_client import MySQLClient
from owl_system.data_sync.synchronizer import DataSynchronizer, run_sync_job
from owl_system.data_sync.task import init_scheduler, shutdown_scheduler, run_sync_now

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 为关键模块设置日志级别
logging.getLogger('owl_system.data_sync.research_client').setLevel(logging.DEBUG)
logging.getLogger('owl_system.data_sync.mysql_client').setLevel(logging.DEBUG)
logging.getLogger('owl_system.data_sync.synchronizer').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

def list_tables(args):
    """列出所有可同步的表"""
    config_file = args.config
    config = SyncConfig.from_config_file(config_file)
    
    print("\n可同步的表列表:")
    print(f"{'表名':<30} {'Research表ID':<50} {'状态':<10}")
    print("-" * 90)
    
    for table_key, table_mapping in config.tables.items():
        status = "启用" if table_mapping.enabled else "禁用"
        print(f"{table_mapping.mysql_table_name:<30} {table_mapping.research_table_id:<50} {status:<10}")

def compare_schema(args):
    """比较表结构"""
    config_file = args.config
    config = SyncConfig.from_config_file(config_file)
    table_key = args.table
    
    if table_key not in config.tables:
        print(f"错误：未找到表 {table_key} 的配置")
        return
    
    table_mapping = config.tables[table_key]
    
    # 打印MySQL配置信息用于调试
    print(f"\nMySQL配置信息:")
    print(f"主机: {config.mysql_host}")
    print(f"端口: {config.mysql_port}")
    print(f"用户: {config.mysql_user}")
    print(f"密码: {'已设置' if config.mysql_password else '未设置'}")
    print(f"数据库: {config.mysql_db}")
    
    # 初始化客户端
    research_client = ResearchClient(config)
    mysql_client = MySQLClient(config)
    
    # 获取Research表结构
    print(f"\n正在获取 Research 表 {table_mapping.research_table_id} 的结构...")
    research_schema = research_client.get_table_schema(table_mapping.research_table_id)
    
    if not research_schema:
        print("无法获取 Research 表结构，请检查配置和网络")
        return
    
    # 获取MySQL表结构
    print(f"正在获取 MySQL 表 {table_mapping.mysql_table_name} 的结构...")
    mysql_schema = mysql_client.get_table_schema(table_mapping.mysql_table_name)
    
    if not mysql_schema:
        print("无法获取 MySQL 表结构，请检查配置和数据库连接")
        return
    
    # 显示字段映射
    print("\n字段映射:")
    print(f"{'Research字段':<30} {'类型':<15} {'MySQL字段':<30} {'类型':<15} {'映射状态':<10}")
    print("-" * 100)
    
    field_mappings = table_mapping.field_mappings
    
    # 首先显示已映射的字段
    for research_field, mysql_field in field_mappings.items():
        research_type = research_schema.get(research_field, {}).get('type', '-')
        mysql_info = mysql_schema.get(mysql_field, {})
        mysql_type = mysql_info.get('data_type', '-')
        
        if research_field in research_schema and mysql_field in mysql_schema:
            status = "✓"
        else:
            status = "✗"
        
        print(f"{research_field:<30} {research_type:<15} {mysql_field:<30} {mysql_type:<15} {status:<10}")
    
    # 显示未映射的Research字段
    print("\n未映射的Research字段:")
    for field in research_schema.keys():
        if field not in field_mappings:
            field_type = research_schema[field].get('type', '-')
            print(f"{field:<30} {field_type:<15}")
    
    # 关闭连接
    mysql_client.close()

def sync_table(args):
    """同步指定表"""
    config_file = args.config
    synchronizer = DataSynchronizer(config_file=config_file)
    table_key = args.table
    
    # 检查表是否存在
    if table_key not in synchronizer.config.tables:
        print(f"错误：未找到表 {table_key} 的配置")
        return
    
    # 执行同步
    print(f"\n开始同步表 {table_key}...")
    inserted, updated = synchronizer.synchronize_table(table_key)
    
    print(f"同步完成：插入 {inserted} 条记录，更新 {updated} 条记录")
    
    # 关闭连接
    synchronizer.close()

def sync_all(args):
    """同步所有表"""
    config_file = args.config
    print("\n开始同步所有表...")
    run_sync_job(config_file)
    print("同步任务完成")

def start_scheduler(args):
    """启动定时任务"""
    config_file = args.config
    init_scheduler(config_file)
    print(f"\n定时同步任务已启动")
    
    try:
        # 阻塞主线程
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_scheduler()
        print("\n定时任务已停止")

def add_common_args(parser):
    """添加通用参数"""
    parser.add_argument('--config', help='配置文件路径', default='config.ini')

def main(argv: Optional[List[str]] = None):
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='华为Research数据同步工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 列出表
    list_parser = subparsers.add_parser('list', help='列出所有可同步的表')
    add_common_args(list_parser)
    list_parser.set_defaults(func=list_tables)
    
    # 比较表结构
    compare_parser = subparsers.add_parser('compare', help='比较表结构')
    compare_parser.add_argument('table', help='表名')
    add_common_args(compare_parser)
    compare_parser.set_defaults(func=compare_schema)
    
    # 同步指定表
    sync_parser = subparsers.add_parser('sync', help='同步指定表')
    sync_parser.add_argument('table', help='表名')
    add_common_args(sync_parser)
    sync_parser.set_defaults(func=sync_table)
    
    # 同步所有表
    sync_all_parser = subparsers.add_parser('sync-all', help='同步所有表')
    add_common_args(sync_all_parser)
    sync_all_parser.set_defaults(func=sync_all)
    
    # 启动定时任务
    scheduler_parser = subparsers.add_parser('scheduler', help='启动定时任务')
    add_common_args(scheduler_parser)
    scheduler_parser.set_defaults(func=start_scheduler)
    
    # 解析参数
    args = parser.parse_args(argv)
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 