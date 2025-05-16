#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试华为Research SDK连接的简单程序
"""

import traceback
import configparser
import json
from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterCondition, FilterOperatorType

def test_connection(config_file='mysql_config.ini'):
    """测试华为Research SDK连接
    
    Args:
        config_file: 配置文件路径
    """
    print(f"从配置文件 {config_file} 加载凭证...")
    
    try:
        # 读取配置文件
        config = configparser.ConfigParser()
        with open(config_file, 'r', encoding='utf-8') as f:
            config.read_file(f)
        
        # 获取凭证信息
        access_key = config.get('credentials', 'access_key')
        secret_key = config.get('credentials', 'secret_key')
        
        print(f"成功读取凭证，Access Key: {access_key[:4]}...{access_key[-4:]}")
        
        # 初始化BridgeConfig类
        bridge_config = BridgeConfig("product", access_key, secret_key)
        
        # 连接超时设置
        connect_timeout = 200
        read_timeout = 200
        retry_on_fail = True
        
        # 初始化HttpClientConfig类
        http_config = HttpClientConfig(connect_timeout, read_timeout, retry_on_fail)
        
        print("初始化BridgeClient...")
        bridge_client = BridgeClient(bridge_config, http_config)
        
        print("华为Research SDK初始化成功！")
        
        # 获取项目信息
        print("\n正在获取项目信息...")
        projects = bridge_client.get_bridgedata_provider().list_projects()
        
        if not projects:
            print("未找到任何项目")
            return False
        
        # 显示项目信息
        print(f"\n找到 {len(projects)} 个项目:")
        for i, project in enumerate(projects, 1):
            project_id = project.get('projectId', '无')
            project_code = project.get('projectCode', '无')
            project_name = project.get('projectName', '无')
            
            print(f"\n项目 {i}:")
            print(f"ProjectId: {project_id}")
            print(f"ProjectCode: {project_code}")
            print(f"项目名称: {project_name}")
        
        # 使用第一个项目测试数据表查询
        first_project = projects[0]
        project_id = first_project.get('projectId')
        
        if not project_id:
            print("无法获取项目ID，无法进行数据表查询")
            return False
        
        # 测试表查询
        test_table_id = 't_mnhqsfbc_atrialfibrillationmeasureresult_system'
        print(f"\n正在查询项目 {project_id} 中的表 {test_table_id}...")
        
        # 构造查询条件
        condition = [FilterCondition("id", FilterOperatorType.EXISTS, True)]
        
        # 构造查询请求
        req = SearchTableDataRequest(
            test_table_id,
            filters=condition,
            desired_size=10,
            project_id=project_id
        )
        
        # 定义回调函数
        results = []
        def rows_callback(rows, total_cnt):
            if not isinstance(rows, list):
                print(f"警告：rows参数类型异常 {type(rows)}")
                return
            
            print(f"查询结果：共 {total_cnt} 条记录，返回 {len(rows)} 条")
            results.extend(rows)
            
            # 打印部分数据
            if rows:
                print("\n前5条记录示例:")
                for i, row in enumerate(rows[:5], 1):
                    print(f"\n记录 {i}:")
                    for k, v in row.items():
                        print(f"  {k}: {v}")
        
        # 执行查询
        bridge_client.get_bridgedata_provider().query_table_data(req, callback=rows_callback)
        
        if not results:
            print("未找到任何数据")
        else:
            print(f"\n成功获取 {len(results)} 条记录")
        
        return True
        
    except Exception as e:
        print(f"操作失败: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection() 