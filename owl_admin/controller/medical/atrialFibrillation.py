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
from owl_system.services.medical.AtrialFibrillationService import AtrialFibrillationService
from ... import reg

# 注意：路由已在 owl_system/modules/medical/__init__.py 中注册
# 这里保留函数定义

# 原路由: @reg.api.route('/medical/af/list', methods=['GET'])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('medical:atrialFibrillation:list'))
@JsonSerializer()
def get_atrial_fibrillation_list():
    """获取房颤检测结果列表"""
    try:
        print("="*50)
        print("收到房颤检测列表请求")
        # 获取查询参数
        params = request.args
        print(f"请求参数: {params}")
        user_id = params.get('user_id')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        page_num = int(params.get('pageNum', 1))
        page_size = int(params.get('pageSize', 10))
        
        # 调试信息: 检查服务类
        print("服务类类型:", type(AtrialFibrillationService))
        print("服务类方法:", dir(AtrialFibrillationService))
        print("使用类方法调用get_list")
        
        # 调用服务获取数据
        records, total = AtrialFibrillationService.get_list(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            page_num=page_num,
            page_size=page_size
        )
        
        print(f"查询完成，获取到 {total} 条记录")
        return TableResponse(rows=records, total=total)
    except Exception as e:
        print("="*50)
        print(f"处理请求异常: {str(e)}")
        # 打印调用堆栈以查看错误位置
        traceback.print_exc(file=sys.stdout)
        print("="*50)
        return AjaxResponse.from_error(str(e))

# 原路由: @reg.api.route('/medical/af/sync', methods=['POST', 'OPTIONS'])
@PreAuthorize(HasPerm('medical:atrialFibrillation:sync'))
@Log(title='房颤检测结果', business_type=BusinessType.UPDATE)
def sync_atrial_fibrillation():
    """同步房颤检测结果数据"""
    # 处理OPTIONS请求
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response
        
    try:
        print("="*50)
        print("开始同步房颤检测数据")
        print(f"请求方法: {request.method}")
        print(f"请求头: {request.headers}")
        
        # 初始化同步器
        synchronizer = DataSynchronizer()
        
        # 同步房颤检测结果表
        inserted, updated = synchronizer.synchronize_table('atrial_fibrillation_measure_result')
        
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