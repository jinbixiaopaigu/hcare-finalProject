import uuid
import logging
from datetime import datetime
from flask import request, jsonify
from sqlalchemy import desc

from owl_system.models.medical import ECG
from owl_system.utils.response_utils import success, error
from owl_admin.ext import db
from owl_system.utils.base_api_utils import handle_db_operation
from owl_system.data_sync.synchronizer import DataSynchronizer

logger = logging.getLogger(__name__)

@handle_db_operation
def list_ecg():
    """获取ECG数据列表"""
    params = request.args.to_dict()
    
    # 查询条件
    query = ECG.query
    
    # 用户ID过滤
    if 'userId' in params and params['userId']:
        query = query.filter(ECG.user_id == params['userId'])
    
    # 数据时间范围过滤
    if 'startTime' in params and params['startTime']:
        query = query.filter(ECG.data_time >= params['startTime'])
    if 'endTime' in params and params['endTime']:
        query = query.filter(ECG.data_time <= params['endTime'])
    
    # 分页
    page = int(params.get('pageNum', 1))
    size = int(params.get('pageSize', 10))
    
    # 排序
    query = query.order_by(desc(ECG.data_time))
    
    # 执行查询
    paginate = query.paginate(page=page, per_page=size, error_out=False)
    
    # 构造返回结果
    data = {
        'total': paginate.total,
        'rows': [item.to_dict() for item in paginate.items],
        'page': page,
        'size': size
    }
    
    return success(data=data)

@handle_db_operation
def get_ecg_detail(id):
    """获取ECG数据详情"""
    record = ECG.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)
    
    return success(data=record.to_dict())

@handle_db_operation
def add_ecg():
    """添加ECG数据"""
    data = request.get_json()
    if not data:
        return error(message='无效的请求数据', code=400)
    
    # 创建新记录
    new_record = ECG(
        id=data.get('id') or str(uuid.uuid4()),
        user_id=data.get('userId'),
        record_group_id=data.get('recordGroupId'),
        upload_time=datetime.now(),
        data_time=data.get('dataTime'),
        ecg_path=data.get('ecgPath'),
        external_id=data.get('externalId', 0),
        metadata_version=data.get('metadataVersion', 1)
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    logger.info(f"添加ECG数据成功: {new_record.id}")
    return success(data=new_record.to_dict())

@handle_db_operation
def update_ecg():
    """更新ECG数据"""
    data = request.get_json()
    if not data or 'id' not in data:
        return error(message='无效的请求数据', code=400)
    
    record = ECG.query.get(data['id'])
    if not record:
        return error(message='数据不存在', code=404)
    
    # 更新字段
    if 'userId' in data:
        record.user_id = data['userId']
    if 'recordGroupId' in data:
        record.record_group_id = data['recordGroupId']
    if 'dataTime' in data:
        record.data_time = data['dataTime']
    if 'ecgPath' in data:
        record.ecg_path = data['ecgPath']
    if 'externalId' in data:
        record.external_id = data['externalId']
    if 'metadataVersion' in data:
        record.metadata_version = data['metadataVersion']
    
    db.session.commit()
    
    logger.info(f"更新ECG数据成功: {record.id}")
    return success(data=record.to_dict())

@handle_db_operation
def delete_ecg(id):
    """删除ECG数据"""
    record = ECG.query.get(id)
    if not record:
        return error(message='数据不存在', code=404)
    
    db.session.delete(record)
    db.session.commit()
    
    logger.info(f"删除ECG数据成功: {id}")
    return success(message='删除成功')

@handle_db_operation
def sync_ecg():
    """同步ECG数据"""
    try:
        # 创建同步器
        synchronizer = DataSynchronizer()
        
        # 执行同步
        result = synchronizer.sync_table('ecg')
        
        # 记录同步结果
        logger.info(f"ECG数据同步完成，结果: {result}")
        
        # 返回响应
        return success(data=result, message='ECG数据同步成功')
    except Exception as e:
        logger.error(f"ECG数据同步失败: {str(e)}")
        return error(message=f'ECG数据同步失败: {str(e)}', code=500) 