from flask import request
from owl_admin.ext import db
from owl_system.models.medical.ContinuousBodyTemperature import ContinuousBodyTemperature
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    validate_required_fields,
    handle_db_operation
)
import logging

logger = logging.getLogger(__name__)

def list_continuous_body_temperature():
    """获取持续体温数据列表"""
    try:
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        request_data = request.get_json(silent=True) or {}
        
        print("\n收到持续体温数据列表请求")
        print(f"请求参数: page={page}, pageSize={pageSize}")
        print(f"完整请求参数: {request_data}")

        # 处理时间范围过滤
        data_time_range = request_data.get('data_time_range', [])
        begin_data_time = data_time_range[0] if len(data_time_range) > 0 else None
        end_data_time = data_time_range[1] if len(data_time_range) > 1 else None
        
        print(f"时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 构建查询
        query = ContinuousBodyTemperature.query
        
        # 应用基础过滤器
        if request_data.get('user_id'):
            query = query.filter(ContinuousBodyTemperature.user_id == request_data['user_id'])
            print(f"应用用户ID过滤: {request_data['user_id']}")
            
        # 应用时间范围过滤
        if begin_data_time and end_data_time:
            query = query.filter(ContinuousBodyTemperature.data_time.between(begin_data_time, end_data_time))
            print(f"应用时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 按时间倒序排序
        query = query.order_by(ContinuousBodyTemperature.data_time.desc())

        # 执行分页查询
        print(f"执行查询: {str(query)}")
        pagination = query.paginate(page=page, per_page=pageSize, error_out=False)
        print(f"查询结果: 共{pagination.total}条记录，当前页{len(pagination.items)}条")

        # 转换结果
        items = []
        for item in pagination.items:
            try:
                item_dict = {
                    'id': item.id,
                    'userId': item.user_id,
                    'bodyTemperature': float(item.body_temperature) if item.body_temperature is not None else None,
                    'bodyTemperatureUnit': item.body_temperature_unit,
                    'skinTemperature': float(item.skin_temperature) if item.skin_temperature is not None else None,
                    'skinTemperatureUnit': item.skin_temperature_unit,
                    'measurementPart': item.measurement_part,
                    'dataTime': item.data_time.strftime('%Y-%m-%d %H:%M:%S') if item.data_time else None,
                    'uploadTime': item.upload_time.strftime('%Y-%m-%d %H:%M:%S') if item.upload_time else None
                }
                items.append(item_dict)
                print(f"记录转换结果: {item_dict}")
            except Exception as e:
                logger.error(f"记录转换失败: {str(e)}")
                continue

        return success(data={
            'rows': items,
            'total': pagination.total,
            'page': page,
            'pageSize': pageSize
        })
    except Exception as e:
        logger.error(f"获取持续体温数据列表失败: {str(e)}", exc_info=True)
        return error(message='服务器内部错误', code=500)

def get_continuous_body_temperature_detail(id):
    """获取持续体温数据详情"""
    try:
        data = ContinuousBodyTemperature.query.get(id)
        if not data:
            return error(message='数据不存在', code=404)

        return success(data=data.to_dict())
    except Exception as e:
        logger.error(f"获取持续体温数据详情失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

@handle_db_operation
def add_continuous_body_temperature():
    """新增持续体温数据"""
    data = request.get_json()
    if not data:
        return error(message='无效的请求数据', code=400)

    required_fields = ['user_id', 'body_temperature', 'measurement_part', 'data_time']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result:
        return validation_result

    new_data = ContinuousBodyTemperature(
        user_id=data['user_id'],
        body_temperature=data['body_temperature'],
        measurement_part=data['measurement_part'],
        data_time=data['data_time'],
        body_temperature_unit=data.get('body_temperature_unit', '℃'),
        skin_temperature=data.get('skin_temperature'),
        skin_temperature_unit=data.get('skin_temperature_unit', '℃'),
        board_temperature=data.get('board_temperature'),
        board_temperature_unit=data.get('board_temperature_unit', '℃'),
        ambient_temperature=data.get('ambient_temperature'),
        ambient_temperature_unit=data.get('ambient_temperature_unit', '℃'),
        confidence=data.get('confidence'),
        external_id=data.get('external_id'),
        metadata_version=data.get('metadata_version')
    )

    db.session.add(new_data)
    print(f"新增持续体温数据成功: {new_data.id}")
    return success(data=new_data.to_dict(), code=201)

@handle_db_operation
def update_continuous_body_temperature():
    """更新持续体温数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return error(message='无效的请求数据', code=400)

    record = ContinuousBodyTemperature.query.get(data['id'])
    if not record:
        return error(message='数据不存在', code=404)

    # 更新字段
    update_fields = [
        'body_temperature', 'measurement_part', 'data_time',
        'body_temperature_unit', 'skin_temperature', 'skin_temperature_unit',
        'board_temperature', 'board_temperature_unit',
        'ambient_temperature', 'ambient_temperature_unit',
        'confidence', 'external_id', 'metadata_version'
    ]
    
    for field in update_fields:
        if field in data:
            setattr(record, field, data[field])

    print(f"更新持续体温数据成功: {record.id}")
    return success(data=record.to_dict())

@handle_db_operation
def delete_continuous_body_temperature(id):
    """删除持续体温数据"""
    record = ContinuousBodyTemperature.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)

    db.session.delete(record)
    print(f"删除持续体温数据成功: {id}")
    return success(message='删除成功')
