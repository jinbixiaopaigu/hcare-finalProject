from flask import request
from owl_system.utils.base_api_utils import table_has_column
from owl_system.utils.pagination import Pagination
from owl_system.utils.response import Response
from owl_system.utils.decorators import validate_required_fields

class BaseController:
    """基础控制器，提供通用CRUD操作"""
    
    def __init__(self, model, config):
        """
        初始化基础控制器
        
        Args:
            model: SQLAlchemy模型类
            config: 控制器配置字典，包含:
                - search_fields: 可搜索字段列表
                - required_fields: 必填字段列表
                - update_fields: 可更新字段列表
                - unique_fields: 唯一性校验字段列表
                - sort_fields: 可排序字段列表
        """
        self.model = model
        self.config = config
        
    def list(self):
        """获取列表数据（带分页和筛选）"""
        try:
            # 解析分页参数
            page_num = request.args.get('page_num', 1, type=int)
            page_size = request.args.get('page_size', 10, type=int)
            
            # 构建查询
            query = self.model.query
            
            # 应用筛选条件
            query = self._apply_filters(query)
            
            # 应用排序
            query = self._apply_sorting(query)
            
            # 执行分页查询
            pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
            items = [item.to_dict() for item in pagination.items]
            
            return Response.success({
                'items': items,
                'total': pagination.total
            })
        except Exception as e:
            return Response.error(str(e))
    
    def get_detail(self, id):
        """获取详情"""
        try:
            item = self.model.query.get(id)
            if not item:
                return Response.error('数据不存在')
            return Response.success(item.to_dict())
        except Exception as e:
            return Response.error(str(e))
    
    @validate_required_fields
    def add(self):
        """新增数据"""
        try:
            data = request.get_json()
            
            # 校验数据唯一性
            if not self._validate_unique(data):
                return Response.error('数据已存在')
                
            # 创建新记录
            item = self.model()
            self._update_model(item, data)
            
            return Response.success(item.to_dict(), '新增成功')
        except Exception as e:
            return Response.error(str(e))
    
    @validate_required_fields
    def update(self, id):
        """更新数据"""
        try:
            item = self.model.query.get(id)
            if not item:
                return Response.error('数据不存在')
                
            data = request.get_json()
            
            # 更新记录
            self._update_model(item, data)
            
            return Response.success(item.to_dict(), '更新成功')
        except Exception as e:
            return Response.error(str(e))
    
    def delete(self, id):
        """删除数据"""
        try:
            item = self.model.query.get(id)
            if not item:
                return Response.error('数据不存在')
                
            item.delete()
            return Response.success(None, '删除成功')
        except Exception as e:
            return Response.error(str(e))
    
    def _apply_filters(self, query):
        """应用筛选条件"""
        for field in self.config.get('search_fields', []):
            if field in request.args and request.args[field]:
                if table_has_column(self.model, field):
                    query = query.filter(getattr(self.model, field).like(f'%{request.args[field]}%'))
        return query
    
    def _apply_sorting(self, query):
        """应用排序"""
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order', 'asc')
        
        if sort_field and sort_field in self.config.get('sort_fields', []):
            if table_has_column(self.model, sort_field):
                if sort_order.lower() == 'desc':
                    query = query.order_by(getattr(self.model, sort_field).desc())
                else:
                    query = query.order_by(getattr(self.model, sort_field).asc())
        return query
    
    def _validate_unique(self, data):
        """校验数据唯一性"""
        for field in self.config.get('unique_fields', []):
            if field in data:
                exists = self.model.query.filter(
                    getattr(self.model, field) == data[field]
                ).first()
                if exists:
                    return False
        return True
    
    def _update_model(self, model, data):
        """更新模型数据"""
        for field in self.config.get('update_fields', []):
            if field in data:
                setattr(model, field, data[field])
        model.save()