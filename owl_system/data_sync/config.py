# -*- coding: utf-8 -*-
# @Author  : data-sync

import os
import json
import logging
import configparser
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

@dataclass
class TableMapping:
    """表映射配置"""
    research_table_id: str  # 华为Research表ID
    mysql_table_name: str   # MySQL表名
    field_mappings: Dict[str, str] = field(default_factory=dict)  # 字段映射 {research字段: mysql字段}
    primary_key: str = 'id'  # 主键字段
    last_sync_time: Optional[str] = None  # 上次同步时间
    enabled: bool = True  # 是否启用同步
    
    def __post_init__(self):
        """初始化后检查字段映射"""
        if not self.field_mappings:
            # 默认字段映射，假设字段名相同
            self.field_mappings = {
                "id": "id",
                "healthid": "user_id",
                "recordgroupid": "group_id",
                "uploadtime": "upload_time",
                "recordtime": "data_time",
                "externalid": "external_id",
                "metadataversion": "metadata_version"
            }

@dataclass
class SyncConfig:
    """同步配置"""
    # 华为Research SDK配置
    research_access_key: str
    research_secret_key: str
    research_env: str = "product"
    connect_timeout: int = 200
    read_timeout: int = 200
    retry_on_fail: bool = True
    
    # 项目信息
    project_id: Optional[str] = None
    project_code: Optional[str] = None
    
    # MySQL数据库配置
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_db: str = "hcare-final"
    
    # 同步配置
    batch_size: int = 1000   # 每批次同步的数据量
    sync_interval: int = 30  # 同步间隔（分钟）
    tables: Dict[str, TableMapping] = field(default_factory=dict)  # 表映射配置
    
    @classmethod
    def from_config_file(cls, config_file: str = 'config.ini') -> 'SyncConfig':
        """从配置文件加载配置"""
        logger.info(f"从配置文件 {config_file} 加载配置")
        config = configparser.ConfigParser()
        
        # 尝试多种编码格式打开文件
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1']
        for encoding in encodings:
            try:
                logger.info(f"尝试使用 {encoding} 编码打开配置文件")
                with open(config_file, 'r', encoding=encoding) as f:
                    config.read_file(f)
                logger.info(f"成功使用 {encoding} 编码读取配置文件")
                break  # 如果成功读取，跳出循环
            except UnicodeDecodeError:
                logger.warning(f"{encoding} 编码无法打开配置文件，尝试下一种编码")
                continue  # 尝试下一种编码
            except Exception as e:
                logger.error(f"读取配置文件时出错: {str(e)}")
                raise
        else:
            # 所有编码格式都失败时，尝试二进制读取再解析
            try:
                logger.warning("所有编码尝试均失败，使用默认方式读取配置文件")
                config.read(config_file)
            except Exception as e:
                logger.error(f"无法读取配置文件 {config_file}: {str(e)}")
                raise
        
        # 读取华为Research凭证
        logger.info("读取Research凭证配置")
        credentials = config['credentials']
        access_key = credentials.get('access_key')
        secret_key = credentials.get('secret_key')
        
        # 创建配置实例
        sync_config = cls(
            research_access_key=access_key,
            research_secret_key=secret_key
        )
        
        # 读取数据库配置（如果存在）
        if 'database' in config:
            logger.info("读取数据库配置")
            db_config = config['database']
            sync_config.mysql_host = db_config.get('host', sync_config.mysql_host)
            sync_config.mysql_port = db_config.getint('port', sync_config.mysql_port)
            sync_config.mysql_user = db_config.get('user', sync_config.mysql_user)
            
            # 特别处理密码字段
            password = db_config.get('password')
            if password is not None:
                sync_config.mysql_password = password
                logger.info(f"已从配置文件中读取MySQL密码，长度: {len(password)}")
            else:
                logger.warning("未从配置文件中读取到MySQL密码，使用空字符串")
                
            sync_config.mysql_db = db_config.get('db', sync_config.mysql_db)
        else:
            logger.warning("配置文件中没有 [database] 部分，使用默认数据库配置")
        
        # 读取同步配置（如果存在）
        if 'sync' in config:
            logger.info("读取同步任务配置")
            sync_section = config['sync']
            sync_config.batch_size = sync_section.getint('batch_size', sync_config.batch_size)
            sync_config.sync_interval = sync_section.getint('sync_interval', sync_config.sync_interval)
        
        # 初始化表映射
        sync_config.init_table_mappings()
        
        return sync_config
    
    def init_table_mappings(self):
        """初始化表映射配置"""
        # 房颤测量结果表
        self.tables['atrial_fibrillation_measure_result'] = TableMapping(
            research_table_id='t_mnhqsfbc_atrialfibrillationmeasureresult_system',
            mysql_table_name='atrial_fibrillation_measure_result',
            field_mappings={
                "uniqueid": "id",
                "healthid": "user_id",
                "groupid": "group_id",  
                "uploadtime": "upload_time",
                "recordtime": "data_time",
                "result": "af_result",
                "riskLevel": "risk_level",
                "externalid": "external_id",
                "recordschema": "metadata_version"
            }
        )
        
        # 血氧饱和度表
        self.tables['blood_oxygen_saturation'] = TableMapping(
            research_table_id='t_mnhqsfbc_bloodoxygensaturation_system',
            mysql_table_name='blood_oxygen_saturation',
            field_mappings={
                "uniqueid": "id",
                "healthid": "user_id",
                "groupid": "record_group_id",
                "uploadtime": "upload_time",
                "recordtime": "data_time",
                "externalid": "external_id",
                "recordschema": "metadata_version",
                # 处理嵌套字段
                "oxygenSaturation.oxygenSaturation.value": "spo2_value",
                "oxygenSaturation.oxygenSaturation.unit": "spo2_unit",
                "oxygenSaturation.timeFrame.timestamp": "measurement_time"
            },
            primary_key="id"
        )
        
        # 连续血氧数据表
        self.tables['continuous_blood_oxygen_saturation'] = TableMapping(
            research_table_id='t_mnhqsfbc_continuousbloodoxygensaturation_system',
            mysql_table_name='continuous_blood_oxygen_saturation',
            field_mappings={
                "uniqueid": "id",
                "healthid": "user_id",
                "groupid": "record_group_id",
                "uploadtime": "upload_time",
                "recordtime": "data_time",
                "externalid": "external_id",
                "recordschema": "metadata_version",
                # 处理嵌套字段 - 根据字段结构调整
                "avgOxygenSaturation.oxygenSaturation.value": "spo2_value",
                "avgOxygenSaturation.oxygenSaturation.unit": "spo2_unit",
                "avgOxygenSaturation.timeFrame.timestamp": "measurement_time",
                # 连续血氧数据可能包含的额外字段
                "avgOxygenSaturation.minOxygenSaturation.value": "spo2_min_value",
                "avgOxygenSaturation.minOxygenSaturation.unit": "spo2_min_unit", 
                "avgOxygenSaturation.minOxygenSaturation.timestamp": "spo2_min_time",
                "avgOxygenSaturation.maxOxygenSaturation.value": "spo2_max_value",
                "avgOxygenSaturation.maxOxygenSaturation.unit": "spo2_max_unit",
                "avgOxygenSaturation.maxOxygenSaturation.timestamp": "spo2_max_time",
                # 这里直接使用oxygenSaturation而不是avgOxygenSaturation
                "avgOxygenSaturation.oxygenSaturation.value": "spo2_avg_value",
                "avgOxygenSaturation.oxygenSaturation.unit": "spo2_avg_unit",
                "avgOxygenSaturation.measurementCount": "spo2_measurement_count",
                "avgOxygenSaturation.measurementDuration": "spo2_measurement_duration",
                "avgOxygenSaturation.measurementDuration.unit": "spo2_measurement_duration_unit",
                "avgOxygenSaturation.measurementStatus": "spo2_measurement_status",
                "avgOxygenSaturation.measurementStatusReason": "spo2_measurement_status_reason",
                "avgOxygenSaturation.statisticalMethod": "statistical_method",
                "avgOxygenSaturation.userNotes": "user_notes",
                "avgOxygenSaturation.groupValues": "spo2_group_values",
                "avgOxygenSaturation.measurementType": "measurement_type",
                "avgOxygenSaturation.timeFrame.startTime": "measurement_start_time",
                "avgOxygenSaturation.timeFrame.endTime": "measurement_end_time"
            },
            primary_key="id"
        )
        
        # 连续体温数据表
        self.tables['continuous_body_temperature'] = TableMapping(
            research_table_id='t_mnhqsfbc_continuousbodytemperature_system',
            mysql_table_name='continuous_body_temperature',
            enabled=True,
            field_mappings={
                'uniqueid': 'id',
                'healthid': 'user_id',
                'groupid': 'record_group_id',
                'uploadtime': 'upload_time',
                'recordtime': 'data_time',
                'externalid': 'external_id',
                'recordschema': 'metadata_version',
                'bodyTemperature.bodyTemperature.value': 'body_temperature',
                'bodyTemperature.bodyTemperature.unit': 'body_temperature_unit',
                'bodyTemperature.skinTemperature.value': 'skin_temperature',
                'bodyTemperature.skinTemperature.unit': 'skin_temperature_unit',
                'bodyTemperature.ambientTemperature.value': 'ambient_temperature',
                'bodyTemperature.ambientTemperature.unit': 'ambient_temperature_unit',
                'bodyTemperature.bodyLocation': 'measurement_part',
                'bodyTemperature.confidence': 'confidence'
            }
        )
        
        # 连续心率数据同步配置
        self.tables['continuousheartrate'] = TableMapping(
            research_table_id='t_mnhqsfbc_continuousheartrate_system',
            mysql_table_name='continuousheartrate',
            field_mappings={
                'uniqueid': 'id',
                'healthid': 'user_id',
                'groupid': 'record_group_id',
                'uploadtime': 'upload_time',
                'recordtime': 'data_time',
                                'avgHeartRate.heartRate.value': 'heart_rate_value',                'avgHeartRate.heartRate.unit': 'heart_rate_unit',                'avgHeartRate.timeFrame.startTime': 'measurement_start_time',                'avgHeartRate.timeFrame.endTime': 'measurement_end_time',                'avgHeartRate.timeFrame.timestamp': 'measurement_time',                'avgHeartRate.statisticalMethod': 'statistical_method',                'avgHeartRate.userNotes': 'user_notes',                'avgHeartRate.groupValues': 'heart_rate_group_values',                'avgHeartRate.measurementType': 'measurement_type',                'externalid': 'external_id',                'recordschema': 'metadata_version',                'avgHeartRate.minHeartRate.value': 'heart_rate_min_value',                'avgHeartRate.minHeartRate.unit': 'heart_rate_min_unit',                'avgHeartRate.minHeartRate.timestamp': 'heart_rate_min_time',                'avgHeartRate.maxHeartRate.value': 'heart_rate_max_value',                'avgHeartRate.maxHeartRate.unit': 'heart_rate_max_unit',                'avgHeartRate.maxHeartRate.timestamp': 'heart_rate_max_time',                'avgHeartRate.avgHeartRate.value': 'heart_rate_avg_value',                'avgHeartRate.avgHeartRate.unit': 'heart_rate_avg_unit',                'avgHeartRate.measurementCount': 'heart_rate_measurement_count',                'avgHeartRate.measurementDuration': 'heart_rate_measurement_duration',                'avgHeartRate.measurementDuration.unit': 'heart_rate_measurement_duration_unit',                'avgHeartRate.measurementStatus': 'heart_rate_measurement_status',                'avgHeartRate.measurementStatusReason': 'heart_rate_measurement_status_reason'
            },
            primary_key='id',
            enabled=True
        )
        
        # 可以继续添加其他表的映射... 

# 连续心率数据同步配置
CONTINUOUS_HEART_RATE_SYNC_CONFIG = {
    'table_name': 'continuousheartrate',
    'field_mappings': {
        'id': 'id',
        'user_id': 'userId',
        'record_group_id': 'recordGroupId',
        'upload_time': 'uploadTime',
        'data_time': 'dataTime',
        'heart_rate_value': 'heartRateValue',
        'heart_rate_unit': 'heartRateUnit',
        'measurement_start_time': 'measurementStartTime',
        'measurement_end_time': 'measurementEndTime',
        'measurement_time': 'measurementTime',
        'statistical_method': 'statisticalMethod',
        'user_notes': 'userNotes',
        'heart_rate_group_values': 'heartRateGroupValues',
        'measurement_type': 'measurementType',
        'external_id': 'externalId',
        'metadata_version': 'metadataVersion',
        'heart_rate_min_value': 'heartRateMinValue',
        'heart_rate_min_unit': 'heartRateMinUnit',
        'heart_rate_min_time': 'heartRateMinTime',
        'heart_rate_max_value': 'heartRateMaxValue',
        'heart_rate_max_unit': 'heartRateMaxUnit',
        'heart_rate_max_time': 'heartRateMaxTime',
        'heart_rate_avg_value': 'heartRateAvgValue',
        'heart_rate_avg_unit': 'heartRateAvgUnit',
        'heart_rate_measurement_count': 'heartRateMeasurementCount',
        'heart_rate_measurement_duration': 'heartRateMeasurementDuration',
        'heart_rate_measurement_duration_unit': 'heartRateMeasurementDurationUnit',
        'heart_rate_measurement_status': 'heartRateMeasurementStatus',
        'heart_rate_measurement_status_reason': 'heartRateMeasurementStatusReason'
    },
    'required_fields': ['id', 'user_id', 'data_time'],
    'unique_fields': ['id'],
    'time_fields': ['upload_time', 'data_time', 'measurement_start_time', 'measurement_end_time', 'measurement_time', 'heart_rate_min_time', 'heart_rate_max_time']
} 