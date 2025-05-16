from flask import request
from owl_admin.ext import db
from owl_system.models.medical.ContinuousRRI import ContinuousRRI
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    validate_required_fields,
    handle_db_operation
)
from owl_system.data_sync.synchronizer import DataSynchronizer
import logging

logger = logging.getLogger(__name__)

def list_continuous_rri():
    """获取连续RRI数据列表"""
    try:
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        request_data = request.get_json(silent=True) or {}
        
        logger.info("\n收到连续RRI数据列表请求")
        logger.info(f"请求参数: page={page}, pageSize={pageSize}")
        logger.debug(f"完整请求参数: {request_data}")

        # 处理时间范围过滤
        data_time_range = request_data.get('data_time_range', [])
        begin_data_time = data_time_range[0] if len(data_time_range) > 0 else None
        end_data_time = data_time_range[1] if len(data_time_range) > 1 else None
        
        logger.info(f"时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 构建查询
        query = ContinuousRRI.query
        
        # 应用基础过滤器
        if request_data.get('user_id'):
            query = query.filter(ContinuousRRI.user_id == request_data['user_id'])
            logger.info(f"应用用户ID过滤: {request_data['user_id']}")
            
        # 应用时间范围过滤
        if begin_data_time and end_data_time:
            query = query.filter(ContinuousRRI.data_time.between(begin_data_time, end_data_time))
            logger.info(f"应用时间范围过滤: {begin_data_time} 至 {end_data_time}")

        # 按时间倒序排序
        query = query.order_by(ContinuousRRI.data_time.desc())

        # 执行分页查询
        logger.info(f"执行查询: {str(query)}")
        pagination = query.paginate(page=page, per_page=pageSize, error_out=False)
        logger.info(f"查询结果: 共{pagination.total}条记录，当前页{len(pagination.items)}条")

        # 转换结果
        items = []
        for item in pagination.items:
            try:
                items.append(item.to_dict())
                logger.debug(f"记录转换结果: {items[-1]}")
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
        logger.error(f"获取连续RRI数据列表失败: {str(e)}", exc_info=True)
        return error(message='服务器内部错误', code=500)

def get_continuous_rri_detail(id):
    """获取连续RRI数据详情"""
    try:
        data = ContinuousRRI.query.get(id)
        if not data:
            return error(message='数据不存在', code=404)

        return success(data=data.to_dict())
    except Exception as e:
        logger.error(f"获取连续RRI数据详情失败: {str(e)}")
        return error(message='服务器内部错误', code=500)

@handle_db_operation
def add_continuous_rri():
    """新增连续RRI数据"""
    data = request.get_json()
    if not data:
        return error(message='无效的请求数据', code=400)

    required_fields = ['user_id', 'data_time', 'rri_data']
    validation_result = validate_required_fields(data, required_fields)
    if validation_result:
        return validation_result

    new_data = ContinuousRRI(
        user_id=data['user_id'],
        data_time=data['data_time'],
        rri_data=data['rri_data'],
        record_group_id=data.get('recordGroupId'),
        upload_time=data.get('uploadTime'),
        external_id=data.get('externalId'),
        metadata_version=data.get('metadataVersion', 1)
    )

    db.session.add(new_data)
    logger.info(f"新增连续RRI数据成功: {new_data.id}")
    return success(data=new_data.to_dict(), code=201)

@handle_db_operation
def update_continuous_rri():
    """更新连续RRI数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return error(message='无效的请求数据', code=400)

    record = ContinuousRRI.query.get(data['id'])
    if not record:
        return error(message='数据不存在', code=404)

    # 更新字段
    update_fields = [
        'data_time', 'rri_data', 'record_group_id',
        'upload_time', 'external_id', 'metadata_version'
    ]
    
    for field in update_fields:
        if field in data:
            setattr(record, field, data[field])

    logger.info(f"更新连续RRI数据成功: {record.id}")
    return success(data=record.to_dict())

@handle_db_operation
def delete_continuous_rri(id):
    """删除连续RRI数据"""
    record = ContinuousRRI.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)

    db.session.delete(record)
    logger.info(f"删除连续RRI数据成功: {id}")
    return success(message='删除成功')

@handle_db_operation
def sync_continuous_rri():
    """同步连续RRI数据"""
    try:
        logger.info("开始同步连续RRI数据")
        logger.info("初始化数据同步器...")
        synchronizer = DataSynchronizer()
        
        logger.info("调用同步方法，表键名: continuousrri")
        result = synchronizer.sync_data('continuousrri')
        
        logger.info(f"同步结果: {result}")
        
        if result.get('success'):
            inserted = result.get('inserted', 0)
            updated = result.get('updated', 0)
            logger.info(f"同步连续RRI数据成功: 新增 {inserted} 条，更新 {updated} 条")
            return success(data=result, message='同步成功')
        else:
            error_msg = result.get('message', '未知错误')
            logger.error(f"同步连续RRI数据失败: {error_msg}")
            return error(message=error_msg, code=500)
    except Exception as e:
        logger.error(f"同步连续RRI数据时发生错误: {str(e)}", exc_info=True)
        return error(message='同步失败：' + str(e), code=500) 