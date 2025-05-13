# 持续体温控制器配置
from owl_system.models.medical import ContinuousBodyTemperature

CONTINUOUS_BODY_TEMPERATURE_CONFIG = {
    # 可搜索字段
    'search_fields': [
        'user_id',
        'measurement_part',
        'data_time',
        'upload_time'
    ],
    
    # 必填字段
    'required_fields': [
        'user_id',
        'measurement_part',
        'body_temperature',
        'data_time'
    ],
    
    # 可更新字段
    'update_fields': [
        'user_id',
        'record_group_id',
        'upload_time',
        'data_time',
        'measurement_part',
        'body_temperature',
        'body_temperature_unit',
        'skin_temperature',
        'skin_temperature_unit',
        'board_temperature',
        'board_temperature_unit',
        'ambient_temperature',
        'ambient_temperature_unit',
        'confidence',
        'external_id',
        'metadata_version'
    ],
    
    # 唯一性校验字段
    'unique_fields': [],
    
    # 可排序字段
    'sort_fields': [
        'data_time',
        'upload_time',
        'user_id'
    ]
}