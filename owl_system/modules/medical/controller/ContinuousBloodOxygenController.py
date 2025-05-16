from flask import request
from owl_admin.ext import db
from owl_system.models.medical.ContinuousBloodOxygenSaturation import ContinuousBloodOxygenSaturation
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    validate_required_fields,
    handle_db_operation
)
import logging

logger = logging.getLogger(__name__)

def list_continuous_blood_oxygen():
    """获取连续血氧饱和度数据列表"""
    try:
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        request_data = request.get_json(silent=True) or {}
        
        logger.info("\n收到连续血氧数据列表请求")
        logger.info(f"请求参数: page={page}, pageSize={pageSize}")
        logger.debug(f"完整请求参数: {request_data}")

        # 处理时间范围过滤
        data_time_range = request_data.get('data_time_range', [])
        begin_data_time = data_time_range[0] if len(data_time_range) > 0 else None
        end_data_time = data_time_range[1] if len(data_time_range) > 1 else None
        
        logger.info(f"时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 构建查询
        query = ContinuousBloodOxygenSaturation.query
        
        # 应用基础过滤器
        if request_data.get('user_id'):
            query = query.filter(ContinuousBloodOxygenSaturation.user_id == request_data['user_id'])
            logger.info(f"应用用户ID过滤: {request_data['user_id']}")
            
        # 应用时间范围过滤
        if begin_data_time and end_data_time:
            query = query.filter(ContinuousBloodOxygenSaturation.data_time.between(begin_data_time, end_data_time))
            logger.info(f"应用时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 按时间倒序排序
        query = query.order_by(ContinuousBloodOxygenSaturation.data_time.desc())

        # 执行分页查询
        logger.info(f"执行查询: {str(query)}")
        pagination = query.paginate(page=page, per_page=pageSize, error_out=False)
        logger.info(f"查询结果: 共{pagination.total}条记录，当前页{len(pagination.items)}条")

        # 转换结果
        items = []
        for item in pagination.items:
            try:
                item_dict = {
                    'id': item.id,
                    'userId': item.user_id,
                    'spo2Value': float(item.spo2_value) if item.spo2_value is not None else None,
                    'spo2Unit': item.spo2_unit,
                    'spo2AvgValue': float(item.spo2_avg_value) if item.spo2_avg_value is not None else None,
                    'spo2AvgUnit': item.spo2_avg_unit,
                    'spo2MinValue': float(item.spo2_min_value) if item.spo2_min_value is not None else None,
                    'spo2MinUnit': item.spo2_min_unit,
                    'spo2MaxValue': float(item.spo2_max_value) if item.spo2_max_value is not None else None,
                    'spo2MaxUnit': item.spo2_max_unit,
                    'spo2MeasurementCount': item.spo2_measurement_count,
                    'spo2MeasurementDuration': item.spo2_measurement_duration,
                    'spo2MeasurementDurationUnit': item.spo2_measurement_duration_unit,
                    'measurementType': item.measurement_type,
                    'dataTime': item.data_time.strftime('%Y-%m-%d %H:%M:%S') if item.data_time else None,
                    'uploadTime': item.upload_time.strftime('%Y-%m-%d %H:%M:%S') if item.upload_time else None,
                    'userNotes': item.user_notes
                }
                items.append(item_dict)
                logger.debug(f"记录转换结果: {item_dict}")
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
        logger.error(f"获取连续血氧数据列表失败: {str(e)}", exc_info=True)
        return error(message='服务器内部错误', code=500)

def get_continuous_blood_oxygen_detail(id):
    """获取连续血氧饱和度数据详情"""
    try:
        data = ContinuousBloodOxygenSaturation.query.get(id)
        if not data:
            return error(message='数据不存在', code=404)

        return success(data=data.to_dict())
    except Exception as e:
        logger.error(f"获取连续血氧数据详情失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

@handle_db_operation
def add_continuous_blood_oxygen():
    """新增连续血氧饱和度数据"""
    data = request.get_json()
    if not data:
        return error(message='无效的请求数据', code=400)

    required_fields = ['user_id', 'spo2_value', 'data_time']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result:
        return validation_result

    new_data = ContinuousBloodOxygenSaturation(
        user_id=data['user_id'],
        spo2_value=data['spo2_value'],
        data_time=data['data_time']
    )

    db.session.add(new_data)
    logger.info(f"新增连续血氧数据成功: {new_data.id}")
    return success(data=new_data.to_dict(), code=201)

@handle_db_operation
def update_continuous_blood_oxygen():
    """更新连续血氧饱和度数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return error(message='无效的请求数据', code=400)

    record = ContinuousBloodOxygenSaturation.query.get(data['id'])
    if not record:
        return error(message='数据不存在', code=404)

    # 更新字段
    if 'spo2_value' in data:
        record.spo2_value = data['spo2_value']
    if 'data_time' in data:
        record.data_time = data['data_time']

    logger.info(f"更新连续血氧数据成功: {record.id}")
    return success(data=record.to_dict())

@handle_db_operation
def delete_continuous_blood_oxygen(id):
    """删除连续血氧饱和度数据"""
    record = ContinuousBloodOxygenSaturation.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)

    db.session.delete(record)
    logger.info(f"删除连续血氧数据成功: {id}")
    return success(message='删除成功')