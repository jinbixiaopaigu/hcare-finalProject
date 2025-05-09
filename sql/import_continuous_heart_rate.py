#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建continuous_heart_rate表"""
    sql = """
    CREATE TABLE IF NOT EXISTS ContinuousHeartRate (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255),
        record_group_id VARCHAR(255),
        upload_time DATETIME,
        data_time DATETIME,
        heart_rate_value FLOAT,
        heart_rate_unit VARCHAR(50),
        measurement_start_time DATETIME,
        measurement_end_time DATETIME,
        measurement_time DATETIME,
        statistical_method VARCHAR(255),
        user_notes TEXT,
        heart_rate_group_values TEXT,
        measurement_type VARCHAR(255),
        external_id VARCHAR(255),
        metadata_version INT,
        heart_rate_min_value FLOAT,
        heart_rate_min_unit VARCHAR(50),
        heart_rate_min_time DATETIME,
        heart_rate_max_value FLOAT,
        heart_rate_max_unit VARCHAR(50),
        heart_rate_max_time DATETIME,
        heart_rate_avg_value FLOAT,
        heart_rate_avg_unit VARCHAR(50),
        heart_rate_measurement_count INT,
        heart_rate_measurement_duration INT,
        heart_rate_measurement_duration_unit VARCHAR(50),
        heart_rate_measurement_status VARCHAR(255),
        heart_rate_measurement_status_reason TEXT
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
            with open('sql/ContinuousHeartRate.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                print("CSV文件列名:", reader.fieldnames)
                batch = []
                
                for row in reader:
                    try:
                        # 处理数据 - 使用CSV中实际的字段名
                        batch.append((
                            row['数据唯一ID'],
                            row['用户ID'],
                            row['记录分组ID'] if '记录分组ID' in row and row['记录分组ID'].strip() else None,
                            row['上传时间'],
                            row['数据时间'],
                            float(row['心率值(bpm)']) if '心率值(bpm)' in row and row['心率值(bpm)'].strip() else None,
                            row['心率值单位'] if '心率值单位' in row and row['心率值单位'].strip() else None,
                            row['心率值.测量开始时间'] if '心率值.测量开始时间' in row and row['心率值.测量开始时间'].strip() else None,
                            row['心率值.测量结束时间'] if '心率值.测量结束时间' in row and row['心率值.测量结束时间'].strip() else None,
                            row['心率值.测量时间'] if '心率值.测量时间' in row and row['心率值.测量时间'].strip() else None,
                            row['心率值.统计方式'] if '心率值.统计方式' in row and row['心率值.统计方式'].strip() else None,
                            row['心率值.用户备注'] if '心率值.用户备注' in row and row['心率值.用户备注'].strip() else None,
                            None,  # 心率组值(原字段不存在)
                            None,  # 测量类型(原字段不存在)
                            row['外部ID'] if '外部ID' in row else None,
                            int(row['元数据版本']) if '元数据版本' in row and row['元数据版本'].strip() else None,
                            float(row['最小心率值(bpm)']) if '最小心率值(bpm)' in row and row['最小心率值(bpm)'].strip() else None,
                            row['最小心率值单位'] if '最小心率值单位' in row and row['最小心率值单位'].strip() else None,
                            row['最小心率.测量时间'] if '最小心率.测量时间' in row and row['最小心率.测量时间'].strip() else None,
                            float(row['最大心率值(bpm)']) if '最大心率值(bpm)' in row and row['最大心率值(bpm)'].strip() else None,
                            row['最大心率值单位'] if '最大心率值单位' in row and row['最大心率值单位'].strip() else None,
                            row['最大心率.测量时间'] if '最大心率.测量时间' in row and row['最大心率.测量时间'].strip() else None,
                            float(row['平均心率值(bpm)']) if '平均心率值(bpm)' in row and row['平均心率值(bpm)'].strip() else None,
                            row['平均心率值单位'] if '平均心率值单位' in row and row['平均心率值单位'].strip() else None,
                            int(row.get('心率测量次数', '0')) if row.get('心率测量次数', '0').strip() else None,
                            int(row.get('心率测量时长', '0')) if row.get('心率测量时长', '0').strip() else None,
                            row.get('心率测量时长单位', '') if row.get('心率测量时长单位', '').strip() else None,
                            row.get('心率测量状态', '') if row.get('心率测量状态', '').strip() else None,
                            row.get('心率测量状态原因', '') if row.get('心率测量状态原因', '').strip() else None
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
    INSERT INTO ContinuousHeartRate (
        id, user_id, record_group_id, upload_time, data_time,
        heart_rate_value, heart_rate_unit, measurement_start_time, measurement_end_time,
        measurement_time, statistical_method, user_notes, heart_rate_group_values,
        measurement_type, external_id, metadata_version, heart_rate_min_value,
        heart_rate_min_unit, heart_rate_min_time, heart_rate_max_value, heart_rate_max_unit,
        heart_rate_max_time, heart_rate_avg_value, heart_rate_avg_unit, heart_rate_measurement_count,
        heart_rate_measurement_duration, heart_rate_measurement_duration_unit,
        heart_rate_measurement_status, heart_rate_measurement_status_reason
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
    print("连续心率数据导入完成")