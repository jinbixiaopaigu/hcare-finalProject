from datetime import datetime
from owl_system.models.medical.AtrialFibrillationMeasureResult import AtrialFibrillationMeasureResult
from owl_system.models import db

class AtrialFibrillationService:
    """房颤检测结果服务类"""
    
    def build_query(self, user_id=None, start_time=None, end_time=None):
        """构建查询条件"""
        query = AtrialFibrillationMeasureResult.query
        
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