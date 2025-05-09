#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

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
            # 读取CSV文件
            with open('sql/BloodOxygenSaturation.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        float(row['血氧饱和度(%)']) if row['血氧饱和度(%)'].strip() else None,
                        row['血氧饱和度单位'] if row['血氧饱和度单位'].strip() else None,
                        row['血氧饱和度.测量开始时间'] if row['血氧饱和度.测量开始时间'].strip() else None,
                        row['血氧饱和度.测量结束时间'] if row['血氧饱和度.测量结束时间'].strip() else None,
                        row['血氧饱和度.测量时间'] if row['血氧饱和度.测量时间'].strip() else None,
                        row['血氧饱和度.统计方式'] if row['血氧饱和度.统计方式'].strip() else None,
                        row['血氧饱和度.用户备注'] if row['血氧饱和度.用户备注'].strip() else None,
                        row['血氧饱和度组值'] if row['血氧饱和度组值'].strip() else None,
                        row['测量类型'] if row['测量类型'].strip() else None,
                        row['外部ID'],
                        int(row['元数据版本'])
                    ))
                    
                    # 批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
                
                # 提交事务
                connection.commit()
                
    finally:
        connection.close()

def insert_data(cursor, batch):
    sql = """
    INSERT INTO blood_oxygen_saturation (
        id, user_id, record_group_id, upload_time, data_time,
        spo2_value, spo2_unit, measurement_start_time, measurement_end_time,
        measurement_time, statistical_method, user_notes, spo2_group_values,
        measurement_type, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("血氧饱和度数据导入完成")