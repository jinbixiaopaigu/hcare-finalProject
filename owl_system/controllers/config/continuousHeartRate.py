# 连续心率控制器配置
from owl_system.models.medical import ContinuousHeartRate

CONTINUOUS_HEART_RATE_CONFIG = {
    # 可搜索字段
    'search_fields': [
        'user_id',
        'data_time',
        'upload_time'
    ],
    
    # 必填字段
    'required_fields': [
        'user_id',
        'heart_rate_value',
        'data_time'
    ],
    
    # 可更新字段
    'update_fields': [
        'user_id',
        'record_group_id',
        'upload_time',
        'data_time',
        'heart_rate_value',
        'heart_rate_unit',
        'measurement_start_time',
        'measurement_end_time',
        'measurement_time',
        'statistical_method',
        'user_notes',
        'heart_rate_group_values',
        'measurement_type',
        'external_id',
        'metadata_version',
        'heart_rate_min_value',
        'heart_rate_min_unit',
        'heart_rate_min_time',
        'heart_rate_max_value',
        'heart_rate_max_unit',
        'heart_rate_max_time',
        'heart_rate_avg_value',
        'heart_rate_avg_unit',
        'heart_rate_measurement_count',
        'heart_rate_measurement_duration',
        'heart_rate_measurement_duration_unit',
        'heart_rate_measurement_status',
        'heart_rate_measurement_status_reason'
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