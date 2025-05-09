#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql
from datetime import datetime

def create_table(cursor):
    """创建DailyHeartRate表，根据DailyHeartRate.csv的结构"""
    sql = """
    CREATE TABLE IF NOT EXISTS DailyHeartRate (
        id VARCHAR(50) PRIMARY KEY,
        user_id VARCHAR(50) NOT NULL,
        record_group_id VARCHAR(50),
        upload_time DATETIME NOT NULL,
        data_time DATETIME NOT NULL,
        max_heart_rate_value INT NOT NULL,
        max_heart_rate_unit VARCHAR(20) NOT NULL,
        min_heart_rate_value INT NOT NULL,
        min_heart_rate_unit VARCHAR(20) NOT NULL,
        resting_heart_rate_value INT,
        resting_heart_rate_unit VARCHAR(20),
        external_id VARCHAR(20),
        metadata_version INT NOT NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_data_time (data_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
    cursor.execute(sql)

def import_data():
    """导入DailyHeartRate数据"""
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1w2e3r4',
        'database': 'hcare-final',
        'charset': 'utf8mb4'
    }
    
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # 创建表
            create_table(cursor)
            print("表DailyHeartRate创建成功")
            
            # 读取CSV文件
            with open('sql/DailyHeartRate.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                batch = []
                total = 0
                
                for row in reader:
                    # 处理数据
                    batch.append((
                        row['数据唯一ID'],
                        row['用户ID'],
                        row['记录分组ID'] if row['记录分组ID'].strip() else None,
                        row['上传时间'],
                        row['数据时间'],
                        int(row['最大心率(beats/min)']),
                        row['最大心率单位'],
                        int(row['最小心率(beats/min)']),
                        row['最小心率单位'],
                        int(row['静息心率(beats/min)']) if row['静息心率(beats/min)'].strip() else None,
                        row['静息心率单位'] if row['静息心率单位'].strip() else None,
                        row['外部ID'],
                        int(row['元数据版本'])
                    ))
                    
                    # 批量插入
                    if len(batch) >= 100:
                        insert_data(cursor, batch)
                        total += len(batch)
                        print(f"已导入 {total} 条记录", end='\r')
                        batch = []
                
                # 插入剩余数据
                if batch:
                    insert_data(cursor, batch)
                    total += len(batch)
                
                # 提交事务
                connection.commit()
                print(f"\n每日心率数据导入完成，共导入{total}条记录")
                
    except Exception as e:
        connection.rollback()
        print("\n导入失败:", e)
    finally:
        connection.close()

def insert_data(cursor, batch):
    """批量插入数据"""
    sql = """
    INSERT INTO DailyHeartRate (
        id, user_id, record_group_id, upload_time, data_time,
        max_heart_rate_value, max_heart_rate_unit, min_heart_rate_value,
        min_heart_rate_unit, resting_heart_rate_value, resting_heart_rate_unit,
        external_id, metadata_version
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s
    )
    """
    cursor.executemany(sql, batch)

if __name__ == '__main__':
    import_data()