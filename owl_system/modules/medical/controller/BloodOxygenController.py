from flask import request
from owl_admin.ext import db
from owl_system.models.medical.BloodOxygenSaturation import BloodOxygenSaturation
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    apply_base_filters,
    apply_date_range_filter,
    validate_required_fields,
    handle_db_operation
)
import logging

logger = logging.getLogger(__name__)

def list_blood_oxygen():
    """获取血氧饱和度数据列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        request_data = request.get_json(silent=True) or {}
        begin_data_time = request_data.get('begin_data_time') or request.args.get('begin_data_time')
        end_data_time = request_data.get('end_data_time') or request.args.get('end_data_time')
        
        logger.info(f"Received params - begin_data_time: {begin_data_time}, end_data_time: {end_data_time}")

        query = BloodOxygenSaturation.query
        query = apply_base_filters(query, BloodOxygenSaturation, ['user_id', 'measurement_type'])
        query = apply_date_range_filter(query, BloodOxygenSaturation, 'data_time', begin_data_time, end_data_time)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = [{
            'id': item.id,
            'user_id': item.user_id,
            'spo2_value': item.spo2_value,
            'measurement_type': item.measurement_type,
            'data_time': item.data_time,
            'upload_time': item.upload_time,
            'user_notes': item.user_notes
        } for item in pagination.items]

        return success(data={
            'items': items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        logger.error(f"获取血氧数据列表失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

def get_blood_oxygen_detail(id):
    """获取血氧饱和度数据详情"""
    try:
        data = BloodOxygenSaturation.query.get(id)
        if not data:
            return make_response(code=404, message='数据不存在')

        return success(data=data.to_dict())
    except Exception as e:
        logger.error(f"获取血氧数据详情失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

@handle_db_operation
def add_blood_oxygen():
    """新增血氧饱和度数据"""
    data = request.get_json()
    if not data:
        return make_response(code=400, message='无效的请求数据')

    required_fields = ['user_id', 'spo2_value', 'data_time']
    for field in required_fields:
        if field not in data:
            return make_response(code=400, message=f'缺少必要字段: {field}')

    new_data = BloodOxygenSaturation(
        user_id=data['user_id'],
        spo2_value=data['spo2_value'],
        data_time=data['data_time'],
        record_group_id=data.get('record_group_id'),
        spo2_unit=data.get('spo2_unit', '%'),
        measurement_type=data.get('measurement_type'),
        user_notes=data.get('user_notes'),
        external_id=data.get('external_id'),
        metadata_version=data.get('metadata_version')
    )

    db.session.add(new_data)
    logger.info(f"新增血氧数据成功: {new_data.id}")
    return success(data=new_data.to_dict(), code=201)

@handle_db_operation
def update_blood_oxygen():
    """更新血氧饱和度数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return make_response(code=400, message='无效的请求数据')

    record = BloodOxygenSaturation.query.get(data['id'])
    if not record:
        return make_response(code=404, message='数据不存在')

    # 更新字段
    if 'spo2_value' in data:
        record.spo2_value = data['spo2_value']
    if 'data_time' in data:
        record.data_time = data['data_time']
    if 'user_notes' in data:
        record.user_notes = data['user_notes']
    if 'measurement_type' in data:
        record.measurement_type = data['measurement_type']

    logger.info(f"更新血氧数据成功: {record.id}")
    return success(data=record.to_dict())

@handle_db_operation
def delete_blood_oxygen(id):
    """删除血氧饱和度数据"""
    record = BloodOxygenSaturation.query.get(id)
    if not record:
        return make_response(code=404, message='数据不存在')

    db.session.delete(record)
    logger.info(f"删除血氧数据成功: {id}")
    return success(message='删除成功')