from sqlalchemy import inspect
from flask import request
from functools import wraps
from datetime import datetime
from owl_admin.ext import db
from owl_system.utils.response_utils import success, error

def table_has_column(model, column_name):
    """
    检查SQLAlchemy模型是否有指定的列
    
    Args:
        model: SQLAlchemy模型类
        column_name: 列名
        
    Returns:
        bool: 如果列存在返回True，否则返回False
    """
    inspector = inspect(model)
    return column_name in [c.key for c in inspector.attrs]

def get_model_columns(model):
    """
    获取SQLAlchemy模型的所有列名
    
    Args:
        model: SQLAlchemy模型类
        
    Returns:
        list: 列名列表
    """
    inspector = inspect(model)
    return [c.key for c in inspector.attrs]

def apply_base_filters(query, model, filter_fields):
    """
    应用基础查询过滤
    
    Args:
        query: SQLAlchemy查询对象
        model: 模型类
        filter_fields: 需要过滤的字段列表
    
    Returns:
        query: 过滤后的查询对象
    """
    request_data = request.get_json(silent=True) or {}
    args = request.args.to_dict()
    
    for field in filter_fields:
        value = request_data.get(field) or args.get(field)
        if value and table_has_column(model, field):
            query = query.filter(getattr(model, field) == value)
    
    return query

def apply_date_range_filter(query, model, date_field, begin_date=None, end_date=None):
    """
    应用日期范围过滤
    
    Args:
        query: SQLAlchemy查询对象
        model: 模型类
        date_field: 日期字段名
        begin_date: 开始日期
        end_date: 结束日期
    
    Returns:
        query: 过滤后的查询对象
    """
    if not table_has_column(model, date_field):
        return query
        
    if begin_date:
        query = query.filter(getattr(model, date_field) >= begin_date)
    if end_date:
        query = query.filter(getattr(model, date_field) <= end_date)
    
    return query

def validate_required_fields(data, required_fields):
    """
    验证必填字段
    
    Args:
        data: 请求数据
        required_fields: 必填字段列表
    
    Returns:
        tuple: (是否验证通过, 错误信息)
    """
    if not data:
        return False, '无效的请求数据'
        
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f'缺少必要字段: {", ".join(missing_fields)}'
    
    return True, None

def handle_db_operation(func):
    """
    数据库操作装饰器
    
    Args:
        func: 被装饰的函数
    
    Returns:
        wrapper: 装饰器函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return error(message=f'数据库操作失败: {str(e)}', code=500)
    return wrapper