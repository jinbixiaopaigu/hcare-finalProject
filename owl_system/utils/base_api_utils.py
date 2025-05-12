from flask import request
from owl_admin.ext import db
from owl_system.utils.response_utils import success, error
import logging

logger = logging.getLogger(__name__)

def apply_base_filters(query, model, search_fields):
    """应用基础筛选条件"""
    request_data = request.get_json(silent=True) or {}
    for field in search_fields:
        field_value = request.args.get(field) or request_data.get(field)
        if field_value:
            if hasattr(model, field):
                query = query.filter(getattr(model, field) == field_value)
    return query

def apply_date_range_filter(query, model, date_field, begin_time, end_time):
    """应用日期范围筛选"""
    if begin_time and end_time:
        logger.info(f"Applying date filter: {begin_time} to {end_time}")
        if hasattr(model, date_field):
            query = query.filter(getattr(model, date_field).between(begin_time, end_time))
    return query

def validate_required_fields(data, required_fields):
    """验证必填字段"""
    for field in required_fields:
        if field not in data:
            return False, f'缺少必要字段: {field}'
    return True, None

def handle_db_operation(func):
    """处理数据库操作的装饰器"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            logger.error(f"数据库操作失败: {str(e)}")
            return error(message='服务器内部错误', code=500)
    return wrapper