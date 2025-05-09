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
            with open('sql/ContinuousBodyTemperature.csv', 'r', encoding='utf-8-sig') as f:
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
                        row['测量部位'],
                        float(row['体温(C)']) if row['体温(C)'].strip() else None,
                        row['体温单位'] if row['体温单位'].strip() else None,
                        float(row['皮肤温度(C)']) if row['皮肤温度(C)'].strip() else None,
                        row['皮肤温度单位'] if row['皮肤温度单位'].strip() else None,
                        float(row['主板温度(C)']) if row['主板温度(C)'].strip() else None,
                        row['主板温度单位'] if row['主板温度单位'].strip() else None,
                        float(row['环境温度(C)']) if row['环境温度(C)'].strip() else None,
                        row['环境温度单位'] if row['环境温度单位'].strip() else None,
                        float(row['bodyTemperature.confidence']) if row['bodyTemperature.confidence'].strip() else None,
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
    INSERT INTO continuous_body_temperature (
        id, user_id, record_group_id, upload_time, data_time, measurement_part,
        body_temperature, body_temperature_unit, skin_temperature, skin_temperature_unit,
        board_temperature, board_temperature_unit, ambient_temperature, ambient_temperature_unit,
        confidence, external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()
    print("数据导入完成")