# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import sys
import traceback
from flask import jsonify, request, make_response
from owl_common.base.model import AjaxResponse, TableResponse
from owl_common.descriptor.serializer import JsonSerializer
from owl_common.descriptor.validator import QueryValidator
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from owl_framework.descriptor.log import Log
from owl_common.domain.enum import BusinessType
from owl_system.data_sync.synchronizer import DataSynchronizer
from ... import reg

# 注意：路由需在 owl_system/modules/medical/__init__.py 中注册

@PreAuthorize(HasPerm('medical:cbo:sync'))
@Log(title='连续血氧饱和度', business_type=BusinessType.UPDATE)
def sync_continuous_blood_oxygen():
    """同步连续血氧饱和度数据"""
    # 处理OPTIONS请求
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response
        
    try:
        print("="*50)
        print("开始同步连续血氧饱和度数据")
        print(f"请求方法: {request.method}")
        print(f"请求头: {request.headers}")
        
        # 初始化同步器
        synchronizer = DataSynchronizer()
        
        # 同步连续血氧饱和度表
        inserted, updated = synchronizer.synchronize_table('continuous_blood_oxygen_saturation')
        
        # 关闭连接
        synchronizer.close()
        
        print(f"同步完成，新增: {inserted}条，更新: {updated}条")
        print("="*50)
        
        # 创建一个Flask响应对象
        response_data = {
            'code': 200,
            'msg': 'success',
            'data': {
                'inserted': inserted,
                'updated': updated
            }
        }
        response = jsonify(response_data)
        
        # 在响应中添加CORS头
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        print("="*50)
        print(f"同步数据异常: {str(e)}")
        traceback.print_exc(file=sys.stdout)
        print("="*50)
        # 创建错误响应
        error_response = jsonify({
            'code': 500,
            'msg': str(e),
            'data': None
        })
        error_response.headers.add("Access-Control-Allow-Origin", "*")
        return error_response 