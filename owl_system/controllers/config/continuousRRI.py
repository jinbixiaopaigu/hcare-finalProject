# 连续RRI控制器配置
from owl_system.models.medical import ContinuousRRI

CONTINUOUS_RRI_CONFIG = {
    # 可搜索字段
    'search_fields': [
        'user_id',
        'data_time',
        'upload_time'
    ],
    
    # 必填字段
    'required_fields': [
        'user_id',
        'rri_data',
        'data_time'
    ],
    
    # 可更新字段
    'update_fields': [
        'user_id',
        'record_group_id',
        'upload_time',
        'data_time',
        'rri_data',
        'external_id',
        'metadata_version'
    ],
    
    # 唯一性校验字段
    'unique_fields': ['id'],
    
    # 可排序字段
    'sort_fields': [
        'data_time',
        'upload_time',
        'user_id'
    ]
} 