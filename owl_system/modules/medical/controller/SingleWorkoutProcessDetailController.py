from flask import request
from owl_admin.ext import db
from owl_system.models.medical.SingleWorkoutProcessDetail import SingleWorkoutProcessDetail
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    apply_base_filters,
    apply_date_range_filter,
    validate_required_fields,
    handle_db_operation
)
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

def list_workout_detail():
    """获取6分钟行走测试数据列表"""
    try:
        # 获取分页参数
        page = request.args.get('page_num', 1, type=int)
        per_page = request.args.get('page_size', 10, type=int)
        
        # 获取筛选条件
        user_id = request.args.get('user_id')
        begin_data_time = request.args.get('begin_data_time')
        end_data_time = request.args.get('end_data_time')
        
        logger.info(f"6分钟行走测试数据查询参数: page={page}, per_page={per_page}, user_id={user_id}, begin_data_time={begin_data_time}, end_data_time={end_data_time}")

        # 构建查询
        query = SingleWorkoutProcessDetail.query
        
        # 添加过滤条件
        if user_id:
            query = query.filter(SingleWorkoutProcessDetail.user_id == user_id)
        
        # 添加日期范围过滤
        if begin_data_time:
            query = query.filter(SingleWorkoutProcessDetail.data_time >= begin_data_time)
        if end_data_time:
            query = query.filter(SingleWorkoutProcessDetail.data_time <= end_data_time)
            
        # 按时间降序排序
        query = query.order_by(SingleWorkoutProcessDetail.data_time.desc())

        # 执行分页查询
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 将查询结果转换为字典列表
        items = [model_to_dict(item) for item in pagination.items]

        return success(data={
            'items': items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        logger.error(f"获取6分钟行走测试数据列表失败: {str(e)}", exc_info=True)
        return error(message=f'获取6分钟行走测试数据列表失败: {str(e)}', code=500)

def get_workout_detail(id):
    """获取6分钟行走测试数据详情"""
    try:
        data = SingleWorkoutProcessDetail.query.get(id)
        if not data:
            return error(message='数据不存在', code=404)

        return success(data=model_to_dict(data))
    except Exception as e:
        logger.error(f"获取6分钟行走测试数据详情失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

@handle_db_operation
def add_workout_detail():
    """新增6分钟行走测试数据"""
    data = request.get_json()
    if not data:
        return error(message='无效的请求数据', code=400)

    required_fields = ['user_id', 'data_time']
    for field in required_fields:
        if field not in data:
            return error(message=f'缺少必要字段: {field}', code=400)

    new_data = SingleWorkoutProcessDetail(
        id=str(uuid.uuid4()),
        user_id=data['user_id'],
        data_time=data['data_time'],
        record_group_id=data.get('record_group_id'),
        upload_time=datetime.now(),
        activity_name=data.get('activity_name', '6分钟行走测试'),
        activity_type=data.get('workout_type', '6分钟行走测试'),
        activity_intensity=data.get('workout_status', 'moderate'),
        activity_duration=data.get('activity_duration'),
        activity_duration_unit=data.get('activity_duration_unit', 'min'),
        activity_distance=data.get('distance'),
        activity_distance_unit=data.get('distance_unit', 'm'),
        activity_calories=data.get('calories'),
        activity_calories_unit=data.get('activity_calories_unit', 'kcal'),
        activity_heart_rate_avg=data.get('heart_rate'),
        activity_heart_rate_avg_unit=data.get('activity_heart_rate_avg_unit', 'bpm'),
        activity_step_count=data.get('step_count'),
        activity_step_count_unit=data.get('activity_step_count_unit', 'steps'),
        activity_speed_avg=data.get('speed'),
        activity_speed_avg_unit=data.get('speed_unit', 'm/s'),
        external_id=data.get('external_id'),
        metadata_version=data.get('metadata_version', 1)
    )

    db.session.add(new_data)
    logger.info(f"新增6分钟行走测试数据成功: {new_data.id}")
    return success(data=model_to_dict(new_data), code=201)

@handle_db_operation
def update_workout_detail():
    """更新6分钟行走测试数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return error(message='无效的请求数据', code=400)

    record = SingleWorkoutProcessDetail.query.get(data['id'])
    if not record:
        return error(message='数据不存在', code=404)

    # 更新字段
    if 'step_count' in data:
        record.activity_step_count = data['step_count']
    if 'distance' in data:
        record.activity_distance = data['distance']
    if 'distance_unit' in data:
        record.activity_distance_unit = data['distance_unit']
    if 'heart_rate' in data:
        record.activity_heart_rate_avg = data['heart_rate']
    if 'speed' in data:
        record.activity_speed_avg = data['speed']
    if 'speed_unit' in data:
        record.activity_speed_avg_unit = data['speed_unit']
    if 'calories' in data:
        record.activity_calories = data['calories']
    if 'workout_type' in data:
        record.activity_type = data['workout_type']
    if 'workout_status' in data:
        record.activity_intensity = data['workout_status']
    if 'data_time' in data:
        record.data_time = data['data_time']
    if 'activity_name' in data:
        record.activity_name = data['activity_name']

    record.updated_at = datetime.now()
    
    logger.info(f"更新6分钟行走测试数据成功: {record.id}")
    return success(data=model_to_dict(record))

@handle_db_operation
def delete_workout_detail(id):
    """删除6分钟行走测试数据"""
    record = SingleWorkoutProcessDetail.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)

    db.session.delete(record)
    logger.info(f"删除6分钟行走测试数据成功: {id}")
    return success(message='删除成功')

def model_to_dict(model):
    """将模型转换为字典"""
    item = model.to_dict()
    return item 