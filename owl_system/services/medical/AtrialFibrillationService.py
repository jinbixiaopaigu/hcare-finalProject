import sys
from datetime import datetime
from typing import List, Tuple, Optional
from owl_system.models.medical.AtrialFibrillationMeasureResult import AtrialFibrillationMeasureResult
from owl_system.models import db

class AtrialFibrillationService:
    """房颤检测结果服务类"""
    
    def __new__(cls, *args, **kwargs):
        print("AtrialFibrillationService 被实例化", file=sys.stderr)
        return super().__new__(cls)
    
    def __init__(self):
        print("AtrialFibrillationService __init__ 被调用", file=sys.stderr)
    
    def __getattr__(self, name):
        print(f"尝试访问不存在的属性: {name}", file=sys.stderr)
        # 如果尝试访问 build_query，提供一个兼容方法
        if name == 'build_query':
            def _build_query(user_id=None, start_time=None, end_time=None):
                print("使用兼容的 build_query 方法", file=sys.stderr)
                return self._compatible_build_query(user_id, start_time, end_time)
            return _build_query
        raise AttributeError(f"{self.__class__.__name__} 没有属性 {name}")
    
    def _compatible_build_query(self, user_id=None, start_time=None, end_time=None):
        """兼容旧版的构建查询条件方法"""
        query = db.session.query(AtrialFibrillationMeasureResult)
        
        if user_id:
            query = query.filter(AtrialFibrillationMeasureResult.user_id == user_id)
            
        if start_time and end_time:
            try:
                start = datetime.strptime(start_time, '%Y-%m-%d')
                end = datetime.strptime(end_time, '%Y-%m-%d')
                query = query.filter(
                    AtrialFibrillationMeasureResult.upload_time >= start,
                    AtrialFibrillationMeasureResult.upload_time <= end
                )
            except ValueError:
                pass
                
        return query.order_by(AtrialFibrillationMeasureResult.upload_time.desc())
    
    @classmethod
    def get_list(cls, user_id: Optional[str] = None, start_time: Optional[str] = None, 
                 end_time: Optional[str] = None, page_num: int = 1, page_size: int = 10) -> Tuple[List[dict], int]:
        """获取房颤检测结果列表
        
        Args:
            user_id: 用户ID
            start_time: 开始时间
            end_time: 结束时间
            page_num: 页码
            page_size: 每页大小
            
        Returns:
            Tuple[List[dict], int]: 记录列表和总数
        """
        print("调用 get_list 类方法", file=sys.stderr)
        # 构建基础查询
        query = db.session.query(AtrialFibrillationMeasureResult)
        
        # 添加查询条件
        if user_id:
            query = query.filter(AtrialFibrillationMeasureResult.user_id == user_id)
            
        if start_time and end_time:
            try:
                start = datetime.strptime(start_time, '%Y-%m-%d')
                end = datetime.strptime(end_time, '%Y-%m-%d')
                query = query.filter(
                    AtrialFibrillationMeasureResult.upload_time >= start,
                    AtrialFibrillationMeasureResult.upload_time <= end
                )
            except ValueError:
                pass
        
        # 计算总数
        total = query.count()
        
        # 添加分页
        query = query.order_by(AtrialFibrillationMeasureResult.upload_time.desc())
        query = query.offset((page_num - 1) * page_size).limit(page_size)
        
        # 执行查询
        results = query.all()
        
        # 转换为字典列表
        records = [result.to_dict() for result in results]
            
        return records, total