from flask import request
from owl_admin.ext import db
from owl_system.models.medical.AtrialFibrillationMeasureResult import AtrialFibrillationMeasureResult
from owl_system.services.medical.AtrialFibrillationService import AtrialFibrillationService
from owl_system.utils.response_utils import success, error

service = AtrialFibrillationService()

def list_atrial_fibrillation():
    try:
        print("收到房颤检测列表请求")  # 调试日志
        page_num = request.args.get('pageNum', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        print(f"请求参数: pageNum={page_num}, pageSize={page_size}")  # 调试日志

        # 真实数据库查询
        query = service.build_query(
            user_id=request.args.get('user_id'),
            start_time=request.args.get('start_time'),
            end_time=request.args.get('end_time')
        )
        
        pagination = query.paginate(
            page=page_num,
            per_page=page_size,
            error_out=False
        )
        
        data = {
            "rows": [item.to_dict() for item in pagination.items],
            "total": int(pagination.total)
        }
        
        print(f"数据库查询结果: {len(data['rows'])}条记录")  # 调试日志
        
        # 无数据时返回空数组
        if not data['rows']:
            print("警告: 查询返回空结果集")
            data['rows'] = []
        return success(data)
        
    except Exception as e:
        print(f"处理请求异常: {str(e)}")  # 错误日志
        return error(str(e))

def get_atrial_fibrillation_detail(id):
    try:
        result = AtrialFibrillationMeasureResult.query.get(id)
        if not result:
            return error('记录不存在', 404)
        return success(result.to_dict())
    except Exception as e:
        return error(str(e))