#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建continuous_blood_oxygen_saturation表"""
    sql = """
    CREATE TABLE IF NOT EXISTS continuous_blood_oxygen_saturation (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255),
        record_group_id VARCHAR(255),
        upload_time DATETIME,
        data_time DATETIME,
        spo2_value FLOAT,
        spo2_unit VARCHAR(50),
        measurement_start_time DATETIME,
        measurement_end_time DATETIME,
        measurement_time DATETIME,
        statistical_method VARCHAR(255),
        user_notes TEXT,
        spo2_group_values TEXT,
        measurement_type VARCHAR(255),
        external_id VARCHAR(255),
        metadata_version INT,
        spo2_min_value FLOAT,
        spo2_min_unit VARCHAR(50),
        spo2_min_time DATETIME,
        spo2_max_value FLOAT,
        spo2_max_unit VARCHAR(50),
        spo2_max_time DATETIME,
        spo2_avg_value FLOAT,
        spo2_avg_unit VARCHAR(50),
        spo2_measurement_count INT,
        spo2_measurement_duration INT,
        spo2_measurement_duration_unit VARCHAR(50),
        spo2_measurement_status VARCHAR(255),
        spo2_measurement_status_reason TEXT
    )
    """
    cursor.execute(sql)

def import_data():
    # 数据库连接配置
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1w2e3r4',
        'database': 'hcare-final',
        'charset': 'utf8mb4'
    }
    
    # 连接数据库
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 创建表
            create_table(cursor)
            
            # 读取CSV文件
            with open('sql/ContinuousBloodOxygenSaturation.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                print("CSV文件列名:", reader.fieldnames)
                batch = []
                
                for row in reader:
                    try:
                        # 处理数据 - 使用CSV中实际的字段名
                        batch.append((
                            row['数据唯一ID'],
                            row['用户ID'],
                            row['记录分组ID'] if row['记录分组ID'].strip() else None,
                            row['上传时间'],
                            row['数据时间'],
                            float(row['平均血氧值(%)']) if row['平均血氧值(%)'].strip() else None,
                            row['平均血氧值单位'] if row['平均血氧值单位'].strip() else None,
                            row['平均血氧值.测量开始时间'] if row['平均血氧值.测量开始时间'].strip() else None,
                            row['平均血氧值.测量结束时间'] if row['平均血氧值.测量结束时间'].strip() else None,
                            row['平均血氧值.测量时间'] if row['平均血氧值.测量时间'].strip() else None,
                            row['平均血氧值.统计方式'] if row['平均血氧值.统计方式'].strip() else None,
                            row['平均血氧值.用户备注'] if row['平均血氧值.用户备注'].strip() else None,
                            None,  # 血氧饱和度组值(原字段不存在)
                            None,  # 测量类型(原字段不存在)
                            row['外部ID'],
                            int(row['元数据版本']) if row['元数据版本'].strip() else None,
                            float(row['最小血氧值']) if row['最小血氧值'].strip() else None,
                            row['最小血氧值单位'] if row['最小血氧值单位'].strip() else None,
                            row['最小血氧.测量时间'] if row['最小血氧.测量时间'].strip() else None,
                            float(row['最大血氧值']) if row['最大血氧值'].strip() else None,
                            row['最大血氧值单位'] if row['最大血氧值单位'].strip() else None,
                            row['最大血氧.测量时间'] if row['最大血氧.测量时间'].strip() else None,
                            float(row['平均血氧值(%)']) if row['平均血氧值(%)'].strip() else None,  # 重复使用平均血氧值
                            row['平均血氧值单位'] if row['平均血氧值单位'].strip() else None,  # 重复使用平均血氧值单位
                            int(row.get('血氧饱和度测量次数', '0')) if row.get('血氧饱和度测量次数', '0').strip() else None,
                            int(row.get('血氧饱和度测量时长', '0')) if row.get('血氧饱和度测量时长', '0').strip() else None,
                            row.get('血氧饱和度测量时长单位', '') if row.get('血氧饱和度测量时长单位', '').strip() else None,
                            row.get('血氧饱和度测量状态', '') if row.get('血氧饱和度测量状态', '').strip() else None,
                            row.get('血氧饱和度测量状态原因', '') if row.get('血氧饱和度测量状态原因', '').strip() else None
                        ))
                    except Exception as e:
                        print(f"处理行时出错: {e}")
                        print(f"问题行数据: {row}")
                        continue
                    
                    # 批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
                
                # 提交事务
                connection.commit()
                
    except Exception as e:
        connection.rollback()
        print(f"导入数据时出错: {e}")
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO continuous_blood_oxygen_saturation (
        id, user_id, record_group_id, upload_time, data_time,
        spo2_value, spo2_unit, measurement_start_time, measurement_end_time,
        measurement_time, statistical_method, user_notes, spo2_group_values,
        measurement_type, external_id, metadata_version, spo2_min_value,
        spo2_min_unit, spo2_min_time, spo2_max_value, spo2_max_unit,
        spo2_max_time, spo2_avg_value, spo2_avg_unit, spo2_measurement_count,
        spo2_measurement_duration, spo2_measurement_duration_unit,
        spo2_measurement_status, spo2_measurement_status_reason
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("连续血氧饱和度数据导入完成")