from flask import request
from owl_admin.ext import db, redis_client
from owl_system.models.medical.ContinuousRRI import ContinuousRRI
from owl_system.utils.response_utils import success, error
from owl_system.utils.base_api_utils import (
    validate_required_fields,
    handle_db_operation
)
from owl_system.data_sync.synchronizer import DataSynchronizer
import logging
import json
from sqlalchemy import and_
from datetime import datetime, timedelta
import hashlib
import pickle

logger = logging.getLogger(__name__)

# 缓存过期时间（秒）
CACHE_EXPIRY = 3600 * 24  # 24小时

def list_continuous_rri():
    """获取连续RRI数据列表"""
    try:
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        
        # 从查询参数中获取日期范围，而不是json
        begin_data_time = request.args.get('begin_data_time')
        end_data_time = request.args.get('end_data_time')
        user_id = request.args.get('user_id')
        
        logger.info("\n收到连续RRI数据列表请求")
        logger.info(f"请求参数: page={page}, pageSize={pageSize}")
        logger.info(f"时间范围参数: begin_data_time={begin_data_time}, end_data_time={end_data_time}")
        logger.debug(f"完整请求参数: {request.args}")

        # 构建查询
        query = ContinuousRRI.query
        
        # 应用基础过滤器
        if user_id:
            query = query.filter(ContinuousRRI.user_id == user_id)
            logger.info(f"应用用户ID过滤: {user_id}")
            
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

def generate_rri_chart():
    """生成RRI数据处理后的数据，供前端图表使用"""
    try:
        # 从请求中获取查询参数
        request_data = request.args.to_dict()
        logger.info(f"收到生成RRI图表数据请求，参数: {request_data}")
        
        # 获取用户ID过滤条件
        user_id = request_data.get('userId')
        
        # 获取时间范围过滤条件
        data_time_range = request_data.get('dataTimeRange', '')
        begin_data_time = None
        end_data_time = None
        
        if data_time_range:
            time_parts = data_time_range.split(',')
            if len(time_parts) >= 2:
                begin_data_time = time_parts[0]
                end_data_time = time_parts[1]
        
        # 获取采样率参数，默认为1（不采样）
        sampling_rate = int(request_data.get('samplingRate', 1))
        # 获取最大点数参数，默认为5000
        max_points = int(request_data.get('maxPoints', 5000))
        # 获取是否使用缓存参数
        use_cache = request_data.get('useCache', 'true').lower() == 'true'
        
        logger.info(f"图表过滤条件: 用户ID={user_id}, 时间范围={begin_data_time}至{end_data_time}, 采样率={sampling_rate}, 最大点数={max_points}, 使用缓存={use_cache}")
        
        # 生成缓存键
        cache_key = generate_cache_key(user_id, begin_data_time, end_data_time, sampling_rate, max_points)
        
        # 如果启用缓存，尝试从缓存获取数据
        if use_cache and redis_client:
            cached_data = get_from_cache(cache_key)
            if cached_data:
                logger.info(f"从缓存中获取到图表数据，缓存键: {cache_key}")
                return success(data=cached_data)
            else:
                logger.info(f"缓存中未找到数据，缓存键: {cache_key}")
        
        # 构建查询条件
        query = ContinuousRRI.query
        
        if user_id:
            query = query.filter(ContinuousRRI.user_id == user_id)
            
        if begin_data_time and end_data_time:
            query = query.filter(ContinuousRRI.data_time.between(begin_data_time, end_data_time))
            
        # 按时间排序
        query = query.order_by(ContinuousRRI.data_time.asc())
        
        # 执行查询
        results = query.all()
        logger.info(f"查询到{len(results)}条RRI记录")
        
        if not results:
            return error(message="未找到符合条件的RRI数据", code=404)
            
        # 处理数据并分组
        start_time = datetime.now()
        groups = group_rri_data(results)
        logger.info(f"数据分为{len(groups)}组")
        
        if not groups:
            return error(message="无法对数据进行分组", code=500)
            
        # 生成每个分组的处理后数据
        chart_data = []
        default_rri_value = 800  # 缺失值的替代值
        
        for i, group in enumerate(groups):
            # 提取组内数据
            processed_data = []
            total_points = 0
            
            for record in group['items']:
                # 获取RRI数据
                rri_data = record.rri_data
                
                # 确保是列表类型
                if not isinstance(rri_data, list):
                    try:
                        if isinstance(rri_data, str):
                            rri_data = json.loads(rri_data)
                    except Exception as e:
                        logger.error(f"解析RRI数据失败: {str(e)}")
                        continue
                
                # 数据量统计
                total_points += len(rri_data)
                
                # 计算动态采样率 - 如果数据量很大，增加采样率
                dynamic_sampling_rate = sampling_rate
                if len(rri_data) > max_points:
                    # 自动计算采样率，确保点数不超过最大值
                    dynamic_sampling_rate = max(sampling_rate, int(len(rri_data) / max_points) + 1)
                    logger.info(f"数据点数({len(rri_data)})超过最大值({max_points})，调整采样率为{dynamic_sampling_rate}")
                
                # 处理每条记录的RRI数据点（使用采样）
                for j, data_point in enumerate(rri_data):
                    # 采样: 只处理采样率的倍数索引的数据点
                    if j % dynamic_sampling_rate != 0:
                        continue
                        
                    if data_point and 'rri' in data_point and 'timeFrame' in data_point and 'timestamp' in data_point['timeFrame']:
                        # 替换零值
                        rri_value = data_point['rri'].get('value', 0)
                        if rri_value == 0:
                            rri_value = default_rri_value
                            
                        # 提取有效数据
                        if rri_value > 0:
                            timestamp = data_point['timeFrame']['timestamp']
                            sqi = data_point.get('sqi', 0)
                            processed_data.append([timestamp, rri_value, sqi])
            
            # 按时间戳排序
            processed_data.sort(key=lambda x: x[0])
            
            # 如果分组数据点仍然过多，再次采样
            final_sampling_rate = 1
            if len(processed_data) > max_points:
                final_sampling_rate = int(len(processed_data) / max_points) + 1
                logger.info(f"分组{i+1}数据点数({len(processed_data)})超过最大值({max_points})，二次采样率为{final_sampling_rate}")
                sampled_data = [processed_data[j] for j in range(0, len(processed_data), final_sampling_rate)]
                processed_data = sampled_data
            
            logger.info(f"分组{i+1}: 原始点数约{total_points}，采样后{len(processed_data)}点")
            
            if processed_data:
                # 计算统计信息
                values = [point[1] for point in processed_data]
                avg_rri = round(sum(values) / len(values))
                min_rri = min(values)
                max_rri = max(values)
                
                # 将图表信息添加到结果中
                chart_data.append({
                    'groupId': i + 1,
                    'startTime': format_time(group['start_time']),
                    'endTime': format_time(group['end_time']),
                    'data': processed_data,  # 直接返回处理后的数据点
                    'validPoints': len(processed_data),
                    'originalPoints': total_points,
                    'avgRRI': avg_rri,
                    'minRRI': min_rri,
                    'maxRRI': max_rri
                })
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        logger.info(f"数据处理耗时: {processing_time:.2f}秒")
        
        # 缓存处理结果
        if use_cache and redis_client:
            save_to_cache(cache_key, chart_data)
            logger.info(f"图表数据已缓存，缓存键: {cache_key}")
        
        return success(data=chart_data)
    except Exception as e:
        logger.error(f"生成RRI图表数据失败: {str(e)}", exc_info=True)
        return error(message=f"生成图表数据失败: {str(e)}", code=500)

def generate_cache_key(user_id, begin_time, end_time, sampling_rate, max_points):
    """生成缓存键"""
    key_parts = [
        'rri_chart',
        f'user_{user_id or "all"}',
        f'begin_{begin_time or "none"}',
        f'end_{end_time or "none"}',
        f'sampling_{sampling_rate}',
        f'maxpoints_{max_points}'
    ]
    key_str = '_'.join(key_parts)
    # 使用MD5生成固定长度的缓存键
    return f"rri:chart:{hashlib.md5(key_str.encode()).hexdigest()}"

def get_from_cache(cache_key):
    """从缓存获取数据"""
    try:
        if not redis_client:
            return None
            
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return pickle.loads(cached_data)
        return None
    except Exception as e:
        logger.error(f"从缓存获取数据失败: {str(e)}")
        return None

def save_to_cache(cache_key, data, expiry=CACHE_EXPIRY):
    """保存数据到缓存"""
    try:
        if not redis_client:
            return False
            
        # 序列化数据
        pickled_data = pickle.dumps(data)
        # 设置到Redis并设置过期时间
        redis_client.setex(cache_key, expiry, pickled_data)
        return True
    except Exception as e:
        logger.error(f"保存数据到缓存失败: {str(e)}")
        return False

def group_rri_data(records):
    """将RRI记录按时间分组"""
    MAX_INTERVAL = 30 * 60  # 30分钟间隔（秒）
    groups = []
    current_group = {
        'items': [],
        'start_time': None,
        'end_time': None
    }
    
    # 确保记录按时间排序
    records.sort(key=lambda x: x.data_time)
    
    for record in records:
        record_time = record.data_time
        
        # 如果当前组为空，或时间间隔在允许范围内
        if not current_group['items'] or (
            (record_time - current_group['end_time']).total_seconds() <= MAX_INTERVAL
        ):
            current_group['items'].append(record)
            
            # 更新组的时间范围
            if current_group['start_time'] is None or record_time < current_group['start_time']:
                current_group['start_time'] = record_time
                
            if current_group['end_time'] is None or record_time > current_group['end_time']:
                current_group['end_time'] = record_time
        else:
            # 如果时间间隔太大，创建新组
            groups.append(current_group)
            current_group = {
                'items': [record],
                'start_time': record_time,
                'end_time': record_time
            }
    
    # 添加最后一组
    if current_group['items']:
        groups.append(current_group)
        
    return groups

def format_time(dt):
    """格式化时间为易读格式"""
    if not dt:
        return "未知时间"
    return dt.strftime("%m-%d %H:%M:%S") 